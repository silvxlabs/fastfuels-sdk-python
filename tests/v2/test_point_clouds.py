"""
tests/v2/test_point_clouds.py
"""

# Core imports
import json
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2.point_clouds import (
    PointCloud,
    _point_cloud_type,
    check_3dep_coverage,
    create_point_cloud_from_3dep,
    create_point_cloud_from_file,
    get_point_cloud,
    list_point_clouds,
)
from fastfuels_sdk.v2.client_library.models import JobStatus, PointCloudType
from fastfuels_sdk.v2.domains import Domain
from fastfuels_sdk.v2.exceptions import NotFoundException

# External imports
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


class TestCreateFrom3dep:
    def test_coverage_preflight(self, covered_3dep_domain):
        coverage = check_3dep_coverage(covered_3dep_domain)

        assert coverage.available is True
        assert coverage.coverage_fraction == pytest.approx(1.0, abs=1e-3)
        assert coverage.estimated_point_count > 0
        assert coverage.point_budget > 0
        assert coverage.exceeds_point_budget is False
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
