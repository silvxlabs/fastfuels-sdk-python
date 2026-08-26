"""
tests/v2/test_point_clouds.py
"""

# Core imports
import json
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.point_clouds import (
    PointCloud,
    _csv,
    _decode_point_cloud_tile,
    _point_cloud_type,
    check_3dep_coverage,
    create_point_cloud_from_3dep,
    create_point_cloud_from_file,
    get_point_cloud,
    list_point_clouds,
)
from fastfuels_sdk.v2.client_library.api.point_clouds import (
    get_point_cloud_data_json,
)
from fastfuels_sdk.v2.client_library.models import JobStatus, PointCloudType
from fastfuels_sdk.v2.client_library.types import UNSET
from fastfuels_sdk.v2.domains import Domain
from fastfuels_sdk.v2.exceptions import NotFoundException, expect

# External imports
import numpy as np
import pytest

# The test_domain fixture is session-scoped and shared (tests/v2/conftest.py).
#
# There is no laspy in the test environment to author a valid LAS/LAZ, so the
# upload tests send a tiny placeholder file: the create call and the signed PUT
# both succeed and the point cloud comes back pending. These tests exercise the
# SDK surface (create + lifecycle), not the server-side LiDAR processing, so
# they never call wait() -- the placeholder would fail parsing.


def _placeholder_laz(directory) -> str:
    path = directory / "scan.laz"
    path.write_bytes(b"\x00" * 64)
    return str(path)


@pytest.fixture(scope="module")
def covered_3dep_domain():
    """A small Bondurant, WY domain with stable 3DEP LiDAR coverage."""
    geojson = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:32612"}},
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [522800, 4720400],
                            [523300, 4720400],
                            [523300, 4720900],
                            [522800, 4720900],
                            [522800, 4720400],
                        ]
                    ],
                },
            }
        ],
    }
    domain = Domain.from_geojson(
        geojson,
        name="test_3dep_point_cloud_domain",
        tags=["sdk-test"],
    )
    yield domain
    domain.delete(force=True)


class TestPointCloudType:
    """Pure unit tests for the scan-type coercion (no API)."""

    def test_string_coerces_to_enum(self):
        assert _point_cloud_type("als") == PointCloudType.ALS
        assert _point_cloud_type("tls") == PointCloudType.TLS

    def test_enum_passes_through(self):
        assert _point_cloud_type(PointCloudType.ALS) is PointCloudType.ALS

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            _point_cloud_type("mls")


class TestCsv:
    """Pure unit tests for the query-parameter CSV helper (no API)."""

    def test_none_passes_through(self):
        assert _csv(None) is None

    def test_string_passes_through(self):
        assert _csv("X,Y,Z") == "X,Y,Z"

    def test_int_sequence_joins(self):
        assert _csv([2, 5]) == "2,5"

    def test_str_sequence_joins(self):
        assert _csv(["X", "Y", "Z"]) == "X,Y,Z"


class TestDecodePointCloudTile:
    """Offline unit tests for binary tile decoding (no API required)."""

    def test_decodes_blocks_in_column_order(self):
        x = np.array([1, 2, 3], dtype="<i4")
        z = np.array([10, 20, 30], dtype="<i4")
        classification = np.array([2, 5, 2], dtype="u1")
        content = x.tobytes() + z.tobytes() + classification.tobytes()
        blocks = _decode_point_cloud_tile(
            content,
            {
                "X-Data-Columns": "X,Z,classification",
                "X-Data-Dtypes": "int32,int32,uint8",
                "X-Data-Count": "3",
            },
        )
        assert list(blocks.keys()) == ["X", "Z", "classification"]
        assert np.array_equal(blocks["X"], x)
        assert np.array_equal(blocks["Z"], z)
        assert np.array_equal(blocks["classification"], classification)
        assert blocks["classification"].dtype == np.uint8

    def test_empty_tile_yields_empty_blocks(self):
        blocks = _decode_point_cloud_tile(
            b"",
            {
                "X-Data-Columns": "X,Y,Z",
                "X-Data-Dtypes": "int32,int32,int32",
                "X-Data-Count": "0",
            },
        )
        assert all(block.size == 0 for block in blocks.values())


class TestDataOutRequiresCompleted:
    """The data-out surface guards on completion without touching the API."""

    def _pending_cloud(self):
        pc = PointCloud.__new__(PointCloud)
        pc.status = JobStatus.PENDING
        return pc

    def test_metadata_requires_completed(self):
        with pytest.raises(ValueError):
            self._pending_cloud().metadata()

    def test_to_numpy_requires_completed(self):
        with pytest.raises(ValueError):
            self._pending_cloud().to_numpy()

    def test_to_dataframe_requires_completed(self):
        with pytest.raises(ValueError):
            self._pending_cloud().to_dataframe()


class TestCreateFrom3dep:
    def test_coverage_preflight(self, covered_3dep_domain):
        coverage = check_3dep_coverage(covered_3dep_domain)

        assert coverage.available is True
        assert coverage.coverage_fraction == pytest.approx(1.0, abs=1e-3)
        assert coverage.estimated_point_count > 0
        assert coverage.datasets

    def test_create_with_pinned_dataset(self, covered_3dep_domain):
        coverage = check_3dep_coverage(covered_3dep_domain)
        dataset = coverage.datasets[0].name
        point_cloud = create_point_cloud_from_3dep(
            covered_3dep_domain,
            datasets=[dataset],
            name="throwaway_3dep_pc",
        )
        try:
            assert isinstance(point_cloud, PointCloud)
            assert point_cloud.domain_id == covered_3dep_domain.id
            assert point_cloud.type_ == PointCloudType.ALS
            assert point_cloud.source["name"] == "3dep"
            assert point_cloud.source["datasets"] == [dataset]
            assert point_cloud.status in (
                JobStatus.PENDING,
                JobStatus.RUNNING,
                JobStatus.COMPLETED,
            )
        finally:
            try:
                point_cloud.delete()
            except NotFoundException:
                pass


class TestCreateAndLifecycle:
    @pytest.fixture(scope="class")
    def uploaded_point_cloud(self, test_domain, tmp_path_factory):
        path = _placeholder_laz(tmp_path_factory.mktemp("pc"))
        pc = create_point_cloud_from_file(
            test_domain, path, point_cloud_type="als", name="throwaway_pc"
        )
        yield pc
        try:
            pc.delete()
        except NotFoundException:
            pass

    def test_create_returns_pending_record(self, uploaded_point_cloud, test_domain):
        pc = uploaded_point_cloud
        assert isinstance(pc, PointCloud)
        assert len(pc.id) > 0
        assert pc.domain_id == test_domain.id
        assert pc.type_ == PointCloudType.ALS
        # Pending at create; the placeholder may later fail processing -- either
        # is fine, we only assert the record was created as a real job.
        assert pc.status in (
            JobStatus.PENDING,
            JobStatus.RUNNING,
            JobStatus.FAILED,
        )

    def test_from_id_and_get_point_cloud(self, uploaded_point_cloud, test_domain):
        fetched = PointCloud.from_id(test_domain.id, uploaded_point_cloud.id)
        assert fetched.id == uploaded_point_cloud.id
        assert (
            get_point_cloud(test_domain, uploaded_point_cloud.id).id
            == uploaded_point_cloud.id
        )

    def test_refresh_returns_self(self, uploaded_point_cloud):
        assert uploaded_point_cloud.refresh() is uploaded_point_cloud

    def test_update_name(self, uploaded_point_cloud, test_domain):
        updated = uploaded_point_cloud.update(name="renamed_pc")
        assert updated is uploaded_point_cloud
        assert (
            get_point_cloud(test_domain, uploaded_point_cloud.id).name == "renamed_pc"
        )

    def test_update_no_fields_makes_no_api_call(self, uploaded_point_cloud):
        assert uploaded_point_cloud.update() is uploaded_point_cloud

    def test_list_membership(self, uploaded_point_cloud, test_domain):
        ids = [pc.id for pc in list_point_clouds(test_domain)]
        assert uploaded_point_cloud.id in ids

    def test_list_cross_domain_membership(self, uploaded_point_cloud):
        ids = [pc.id for pc in list_point_clouds()]
        assert uploaded_point_cloud.id in ids

    def test_to_json(self, uploaded_point_cloud):
        assert (
            json.loads(uploaded_point_cloud.to_json())["id"] == uploaded_point_cloud.id
        )


class TestNotFound:
    def test_from_id_not_found(self, test_domain):
        with pytest.raises(NotFoundException):
            PointCloud.from_id(test_domain.id, uuid4().hex)


class TestDelete:
    def test_delete_then_not_found(self, test_domain, tmp_path):
        pc = create_point_cloud_from_file(
            test_domain, _placeholder_laz(tmp_path), point_cloud_type="tls"
        )
        pc.delete()
        with pytest.raises(NotFoundException):
            PointCloud.from_id(test_domain.id, pc.id)


@pytest.fixture(scope="module")
def completed_3dep_point_cloud(covered_3dep_domain):
    """A completed 3DEP point cloud for reading data out. READ-ONLY."""
    coverage = check_3dep_coverage(covered_3dep_domain)
    point_cloud = create_point_cloud_from_3dep(
        covered_3dep_domain,
        datasets=[coverage.datasets[0].name],
        name="data_out_3dep_pc",
    )
    point_cloud.wait()
    yield point_cloud
    try:
        point_cloud.delete()
    except NotFoundException:
        pass


def _reassemble_xyz_via_json(point_cloud, lod=None, classes=None) -> np.ndarray:
    """Reassemble decoded X/Y/Z from the JSON tile endpoint, independently of
    the binary path used by ``to_numpy``.

    This shares no code with the binary decode: it uses the generated client's
    fully-typed JSON parser (``get_point_cloud_data_json``) rather than
    hand-decoding raw bytes. Comparing the two arrays validates the binary
    decode end to end -- dtype, byte order, block split, and tile paging.
    """
    meta = point_cloud.metadata()
    parts = []
    for tile in meta.tiles:
        response = expect(
            get_point_cloud_data_json.sync_detailed(
                point_cloud.domain_id,
                point_cloud.id,
                tile.tile_x,
                tile.tile_y,
                client=ensure_client(),
                lod=lod if lod is not None else UNSET,
                classes=_csv(classes) if classes is not None else UNSET,
                columns="X,Y,Z",
            )
        )
        n = len(response.data["X"])
        if n == 0:
            continue
        block = np.empty((n, 3), dtype=np.float64)
        for axis, name in enumerate(("X", "Y", "Z")):
            stored = np.array(response.data[name], dtype=np.float64)
            block[:, axis] = stored * response.scales[axis] + response.offsets[axis]
        parts.append(block)
    return np.concatenate(parts) if parts else np.empty((0, 3), dtype=np.float64)


def _max_json_lod(meta, n_columns) -> int:
    """Highest LOD whose busiest tile stays under the JSON value cap (1e6).

    The JSON endpoint caps a response at 1,000,000 numeric values (rows times
    columns); the binary endpoint does not. Pick an LOD both transports can
    serve so the two paths can be compared value for value.
    """
    limit = 1_000_000
    best = 0
    for lod in range(meta.lod_levels):
        worst = max((tile.points_by_lod[lod] for tile in meta.tiles), default=0)
        if worst * n_columns <= limit:
            best = lod
        else:
            break
    return best


def _sorted_rows(points: np.ndarray) -> np.ndarray:
    """Sort an (N, k) array by its columns, so two point sets compare equal
    regardless of the order each transport returned them in."""
    order = np.lexsort(tuple(points[:, i] for i in reversed(range(points.shape[1]))))
    return points[order]


class TestDataOut:
    """Live tests for reading point-cloud data into memory."""

    def test_metadata(self, completed_3dep_point_cloud):
        meta = completed_3dep_point_cloud.metadata()
        assert meta.tiles
        assert meta.lod_levels > 0
        assert len(meta.scales) == 3
        assert len(meta.offsets) == 3
        assert {"X", "Y", "Z"}.issubset(set(meta.columns.additional_keys))

    def test_to_numpy_shape_and_count(self, completed_3dep_point_cloud):
        pc = completed_3dep_point_cloud
        meta = pc.metadata()
        expected = sum(tile.points_by_lod[-1] for tile in meta.tiles)
        points = pc.to_numpy()
        assert points.shape == (expected, 3)
        assert points.dtype == np.float64

    def test_to_numpy_decodes_into_crs_bounds(self, completed_3dep_point_cloud):
        # Decoded X/Y must land within the point cloud's reported horizontal
        # extent; a broken decode (wrong scale/offset/byte order) would not.
        pc = completed_3dep_point_cloud
        meta = pc.metadata()
        points = pc.to_numpy()
        min_x, min_y, max_x, max_y = meta.bounds
        assert points[:, 0].min() >= min_x - 1
        assert points[:, 0].max() <= max_x + 1
        assert points[:, 1].min() >= min_y - 1
        assert points[:, 1].max() <= max_y + 1
        assert points[:, 2].std() > 0

    def test_to_numpy_matches_json_transport(self, completed_3dep_point_cloud):
        # The binary reconstruction must agree, value for value, with an
        # independent reassembly over the JSON tile endpoint. Both are read at
        # an LOD the JSON endpoint can serve without hitting its value cap.
        pc = completed_3dep_point_cloud
        lod = _max_json_lod(pc.metadata(), n_columns=3)
        binary = pc.to_numpy(lod=lod)
        reference = _reassemble_xyz_via_json(pc, lod=lod)
        assert binary.shape == reference.shape
        assert binary.shape[0] > 0
        assert np.allclose(_sorted_rows(binary), _sorted_rows(reference))

    def test_to_numpy_raw_coordinates(self, completed_3dep_point_cloud):
        pc = completed_3dep_point_cloud
        raw = pc.to_numpy(decode_coordinates=False)
        decoded = pc.to_numpy()
        meta = pc.metadata()
        expected = raw.copy()
        for axis in range(3):
            expected[:, axis] = raw[:, axis] * meta.scales[axis] + meta.offsets[axis]
        assert np.allclose(decoded, expected)

    def test_to_numpy_lod_is_subset(self, completed_3dep_point_cloud):
        pc = completed_3dep_point_cloud
        coarse = pc.to_numpy(lod=0)
        full = pc.to_numpy()
        assert coarse.shape[0] <= full.shape[0]
        assert coarse.shape[1] == 3

    def test_to_dataframe_columns_and_length(self, completed_3dep_point_cloud):
        pc = completed_3dep_point_cloud
        df = pc.to_dataframe()
        meta = pc.metadata()
        expected = sum(tile.points_by_lod[-1] for tile in meta.tiles)
        assert len(df) == expected
        assert {"X", "Y", "Z"}.issubset(set(df.columns))

    def test_to_dataframe_column_projection(self, completed_3dep_point_cloud):
        pc = completed_3dep_point_cloud
        df = pc.to_dataframe(columns=["X", "Y", "Z"])
        assert list(df.columns) == ["X", "Y", "Z"]

    def test_classes_filter_returns_subset(self, completed_3dep_point_cloud):
        pc = completed_3dep_point_cloud
        ground = pc.to_dataframe(classes=[2], columns=["X", "Y", "Z", "classification"])
        if not ground.empty:
            assert set(ground["classification"].unique()) <= {2}
        full = pc.to_dataframe(columns=["X", "Y", "Z"])
        assert len(ground) <= len(full)
