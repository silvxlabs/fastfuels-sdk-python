"""
tests/v2/test_grids.py
"""

# Core imports
import inspect
import json
import math
from types import SimpleNamespace
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2 import grids
from fastfuels_sdk.v2.grids import (
    Grid,
    _build_alignment,
    _decode_grid_chunk,
    _domain_id,
    _enum_list,
    _fill_for,
    _opt,
    check_3dep_coverage,
    create_canopy_fuel_grid_from_landfire,
    create_canopy_height_grid_from_meta,
    create_canopy_height_grid_from_naip_chm,
    create_fuel_grid_from_fbfm40_lookup,
    create_fuel_model_grid_from_landfire_fbfm40,
    create_fuel_model_grid_from_landfire_fccs,
    create_grid_from_geotiff,
    create_pim_grid_from_treemap,
    create_topography_grid_from_3dep,
    create_topography_grid_from_landfire,
    create_uniform_grid,
    get_grid,
    list_grids,
)
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.client_library.api.grids import get_grid_data_json
from fastfuels_sdk.v2.client_library.models import (
    BandType,
    GridAlignmentDomainTarget,
    GridAlignmentGridTarget,
    GridAlignmentNativeTarget,
    GridDataArrayFormat,
    GridDataOrder,
    GridModification,
    GridModificationAction,
    GridModificationCondition,
    GridSource,
    JobStatus,
    Modifier,
    Operator,
    ResamplingMethod,
    TopographyBand,
    UploadBandDefinition,
)
from fastfuels_sdk.v2.client_library.types import UNSET
from fastfuels_sdk.v2.exceptions import NotFoundException, expect
from fastfuels_sdk.v2.modifications import mask

# External imports
import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

# The test_domain and completed_topography_grid fixtures are session-scoped
# and shared across modules (tests/v2/conftest.py). They are READ-ONLY:
# tests that mutate or delete create throwaways.


class TestBuildAlignment:
    """Pure unit tests for the alignment-keyword translator (no API)."""

    def test_none_is_unset(self):
        assert _build_alignment() is UNSET

    def test_output_resolution_is_domain_target(self):
        alignment = _build_alignment(output_resolution_m=10)
        assert isinstance(alignment, GridAlignmentDomainTarget)
        assert alignment.resolution == 10

    def test_align_native(self):
        alignment = _build_alignment(align="native")
        assert isinstance(alignment, GridAlignmentNativeTarget)

    def test_align_to_grid_id(self):
        alignment = _build_alignment(align_to="abc123")
        assert isinstance(alignment, GridAlignmentGridTarget)
        assert alignment.grid_id == "abc123"

    def test_align_to_grid_object(self):
        # A Grid (or any object with .id) is accepted, not just an id string
        alignment = _build_alignment(align_to=SimpleNamespace(id="gid"))
        assert alignment.grid_id == "gid"

    def test_resampling_method(self):
        alignment = _build_alignment(output_resolution_m=10, resampling="bilinear")
        assert alignment.method == ResamplingMethod.BILINEAR

    def test_conflicting_targets_raise(self):
        with pytest.raises(ValueError):
            _build_alignment(output_resolution_m=10, align="native")
        with pytest.raises(ValueError):
            _build_alignment(align_to="abc", align="native")

    def test_bad_resampling_raises(self):
        with pytest.raises(ValueError):
            _build_alignment(resampling="not_a_method")

    def test_bad_align_value_raises(self):
        with pytest.raises(ValueError):
            _build_alignment(align="bogus")


class TestHelpers:
    """Pure unit tests for the small request-marshalling helpers (no API)."""

    def test_opt_none_is_unset(self):
        assert _opt(None) is UNSET

    def test_opt_passes_values_through(self):
        assert _opt("x") == "x"
        # 0 and "" are not None, so they pass through unchanged
        assert _opt(0) == 0
        assert _opt("") == ""

    def test_domain_id_from_string(self):
        assert _domain_id("abc123") == "abc123"

    def test_domain_id_from_object(self):
        assert _domain_id(SimpleNamespace(id="gid")) == "gid"

    def test_enum_list_none_is_unset(self):
        assert _enum_list(None, TopographyBand) is UNSET

    def test_enum_list_coerces_strings(self):
        assert _enum_list(["elevation", "slope"], TopographyBand) == [
            TopographyBand.ELEVATION,
            TopographyBand.SLOPE,
        ]

    def test_enum_list_passes_members_through(self):
        assert _enum_list([TopographyBand.ASPECT], TopographyBand) == [
            TopographyBand.ASPECT
        ]

    def test_enum_list_invalid_value_raises(self):
        with pytest.raises(ValueError):
            _enum_list(["not_a_band"], TopographyBand)


class TestFccsSignature:
    """FCCS create reached alignment parity with the other LANDFIRE creators
    (FastFuels-API-v2 #358), so the SDK creator exposes the same kwargs."""

    def test_fccs_exposes_alignment_kwargs(self):
        params = inspect.signature(
            grids.create_fuel_model_grid_from_landfire_fccs
        ).parameters
        for expected in (
            "output_resolution_m",
            "align_to",
            "align",
            "resampling",
            "extent_buffer_cells",
        ):
            assert expected in params

    def test_fbfm40_has_alignment_kwargs(self):
        params = inspect.signature(
            grids.create_fuel_model_grid_from_landfire_fbfm40
        ).parameters
        assert "output_resolution_m" in params
        assert "align_to" in params


class TestCreateTopographyGridFrom3dep:
    def test_create(self, test_domain):
        grid = create_topography_grid_from_3dep(
            test_domain, output_resolution_m=10, name="throwaway_topo"
        )

        # Grid generation is an asynchronous job
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        assert grid.source is not None
        grid.delete()

    def test_completed_fixture(self, completed_topography_grid):
        assert completed_topography_grid.status == JobStatus.COMPLETED
        assert completed_topography_grid.name == "test_topography"
        assert completed_topography_grid.tags == ["test"]
        # The georeference and chunk layout are populated once complete
        assert completed_topography_grid.georeference is not None
        assert len(completed_topography_grid.bands) > 0


class TestCreateTopographyGridFromLandfire:
    def test_create(self, test_domain):
        grid = create_topography_grid_from_landfire(
            test_domain,
            output_resolution_m=30,
            bands=["elevation"],
            name="throwaway_lf_topo",
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        assert grid.source is not None
        grid.delete()


class TestCreateCanopyFuelGridFromLandfire:
    def test_create(self, test_domain):
        grid = create_canopy_fuel_grid_from_landfire(
            test_domain,
            output_resolution_m=30,
            bands=["cbd"],
            name="throwaway_canopy_fuel",
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestCreateCanopyHeightGridFromMeta:
    def test_create(self, test_domain):
        grid = create_canopy_height_grid_from_meta(
            test_domain, output_resolution_m=30, name="throwaway_meta_chm"
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestCreateCanopyHeightGridFromNaipChm:
    def test_create(self, test_domain):
        grid = create_canopy_height_grid_from_naip_chm(
            test_domain, output_resolution_m=30, name="throwaway_naip_chm"
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestCreateFuelModelGridFromLandfireFbfm40:
    def test_create(self, test_domain):
        # remove_non_burnable exercises the string -> enum list coercion
        grid = create_fuel_model_grid_from_landfire_fbfm40(
            test_domain,
            output_resolution_m=30,
            remove_non_burnable=["NB1", "NB2"],
            name="throwaway_fbfm40",
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestMask:
    def test_mask_payload_shape(self):
        # Unit: a single band masks one feature to one replacement value
        mod = mask("feat123", "fbfm", 91, buffer_m=5, target="cell")
        payload = mod.to_dict()
        assert payload["conditions"] == [
            {
                "source": "feature",
                "operator": "within",
                "feature_id": "feat123",
                "buffer_m": 5,
                "target": "cell",
            }
        ]
        assert payload["actions"] == [
            {"band": "fbfm", "modifier": "replace", "value": 91}
        ]

    def test_mask_multiple_bands(self):
        # A list of bands fans out to one action per band, sharing the condition
        mod = mask("feat999", ["fuel_load.1hr", "fuel_depth"])
        bands = [action["band"] for action in mod.to_dict()["actions"]]
        assert bands == ["fuel_load.1hr", "fuel_depth"]

    def test_mask_accepts_feature_object(self):
        # A Feature-like object contributes its id
        mod = mask(SimpleNamespace(id="feat-from-object"), "fbfm")
        assert mod.to_dict()["conditions"][0]["feature_id"] == "feat-from-object"

    def test_mask_applied_to_grid_creation(self, test_domain, completed_road_feature):
        # Live: masking an FBFM40 grid against a completed road feature
        grid = create_fuel_model_grid_from_landfire_fbfm40(
            test_domain,
            output_resolution_m=30,
            modifications=[mask(completed_road_feature, "fbfm", 91, buffer_m=5)],
            name="throwaway_masked_fbfm40",
        )
        assert len(grid.id) > 0
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestCreateFuelModelGridFromLandfireFccs:
    def test_create(self, test_domain):
        grid = create_fuel_model_grid_from_landfire_fccs(
            test_domain, remove_bare_ground=True, name="throwaway_fccs"
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()

    def test_create_with_alignment(self, test_domain):
        # #358 brought FCCS to alignment parity; output_resolution_m anchors
        # output cells to the domain origin, like the other LANDFIRE creators.
        grid = create_fuel_model_grid_from_landfire_fccs(
            test_domain, output_resolution_m=30, name="throwaway_fccs_aligned"
        )
        assert len(grid.id) > 0
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestCreatePimGridFromTreemap:
    def test_create(self, test_domain):
        grid = create_pim_grid_from_treemap(
            test_domain,
            output_resolution_m=30,
            resampling="nearest",
            name="throwaway_treemap",
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        grid.delete()


class TestUploadCreators:
    """The GeoTIFF/NetCDF upload creators need a binary raster whose CRS
    matches the domain CRS. The GeoTIFF path builds one on the fly with
    rasterio; the NetCDF path is deferred (no on-the-fly NetCDF writer here).
    """

    def test_create_grid_from_geotiff(self, test_domain, tmp_path):
        # Build a single-band float GeoTIFF on the domain's lattice and CRS,
        # upload it, and confirm it processes to completion. This exercises the
        # signed-upload header contract end-to-end (the unit-level check lives
        # in tests/v2/test_uploads.py); the grid upload path was missing the
        # GCS x-goog-content-length-range header until that was centralized.
        minx, miny, maxx, maxy = test_domain.bbox
        crs = test_domain.get_lattice(resolution=30.0).crs
        res = 30.0
        width = max(1, math.ceil((maxx - minx) / res))
        height = max(1, math.ceil((maxy - miny) / res))
        data = np.arange(width * height, dtype="float32").reshape(height, width)
        path = tmp_path / "elevation.tif"
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=1,
            dtype="float32",
            crs=crs,
            transform=from_origin(minx, maxy, res, res),
        ) as dst:
            dst.write(data, 1)

        grid = create_grid_from_geotiff(
            test_domain,
            str(path),
            bands=[UploadBandDefinition(key="elevation", type_=BandType.CONTINUOUS)],
            name="throwaway_geotiff",
        )
        assert grid.domain_id == test_domain.id
        grid.wait()
        assert grid.status == JobStatus.COMPLETED
        assert [b.key for b in grid.bands] == ["elevation"]
        grid.delete()

    @pytest.mark.skip(
        reason="needs an on-the-fly NetCDF writer matching the domain CRS"
    )
    def test_create_grid_from_netcdf(self, test_domain):
        pass


class TestCreateUniformGrid:
    def test_create(self, test_domain):
        grid = create_uniform_grid(
            test_domain,
            resolution_m=30,
            bands={"fuel_depth": 0.5, "fuel_load.1hr": 0.2},
            name="throwaway_uniform",
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
        assert grid.status in (
            JobStatus.PENDING,
            JobStatus.RUNNING,
            JobStatus.COMPLETED,
        )
        grid.delete()

    def test_invalid_band_key(self, test_domain):
        with pytest.raises(ValueError):
            create_uniform_grid(test_domain, resolution_m=30, bands={"not_a_band": 1.0})


class TestFromId:
    def test_success(self, test_domain, completed_topography_grid):
        grid = Grid.from_id(test_domain.id, completed_topography_grid.id)
        assert grid.id == completed_topography_grid.id
        assert grid.domain_id == test_domain.id

    def test_not_found(self, test_domain):
        with pytest.raises(NotFoundException):
            Grid.from_id(test_domain.id, uuid4().hex)


class TestGetGrid:
    def test_get_grid_returns_new_instance(
        self, test_domain, completed_topography_grid
    ):
        grid = get_grid(test_domain, completed_topography_grid.id)
        assert grid.id == completed_topography_grid.id
        assert grid is not completed_topography_grid


class TestRefreshGrid:
    def test_refresh_returns_self(self, completed_topography_grid):
        refreshed = completed_topography_grid.refresh()
        assert refreshed is completed_topography_grid
        assert refreshed.id == completed_topography_grid.id


class TestWait:
    def test_timeout(self, test_domain):
        grid = create_topography_grid_from_3dep(test_domain, output_resolution_m=10)
        if grid.status == JobStatus.COMPLETED:
            grid.delete()
            pytest.skip("grid completed too quickly to test the timeout")
        with pytest.raises(TimeoutError):
            grid.wait(timeout=0)
        grid.delete()


class TestUpdateGrid:
    @pytest.fixture(scope="class")
    def update_grid(self, test_domain):
        """A throwaway grid to mutate (the shared fixtures are read-only)."""
        grid = create_uniform_grid(
            test_domain,
            resolution_m=30,
            bands={"fuel_depth": 0.5},
            name="update_target",
        )
        yield grid
        grid.delete()

    def test_update_name(self, test_domain, update_grid):
        # update() mutates in place and returns self (chains)
        updated = update_grid.update(name="updated_name")
        assert updated is update_grid
        assert update_grid.name == "updated_name"
        assert get_grid(test_domain, update_grid.id).name == "updated_name"

    def test_update_tags(self, update_grid):
        update_grid.update(tags=["updated"])
        assert update_grid.tags == ["updated"]

    def test_update_no_fields_makes_no_api_call(self, update_grid):
        assert update_grid.update() is update_grid


class TestResample:
    def test_resample_returns_new_pending_grid(self, completed_topography_grid):
        resampled = completed_topography_grid.resample(
            output_resolution_m=30, name="resampled"
        )
        assert isinstance(resampled, Grid)
        assert resampled.id != completed_topography_grid.id
        assert resampled.domain_id == completed_topography_grid.domain_id
        resampled.delete()

    def test_resample_requires_completed_source(self, test_domain):
        grid = create_topography_grid_from_3dep(test_domain, output_resolution_m=10)
        if grid.status == JobStatus.COMPLETED:
            grid.delete()
            pytest.skip("grid completed too quickly to test the guard")
        with pytest.raises(ValueError, match="resample"):
            grid.resample(output_resolution_m=30)
        grid.delete()


class TestApplyModifications:
    def test_apply_modifications_requires_completed(self):
        # Pure guard: a non-completed grid raises before any API call.
        grid = Grid(
            id="g",
            domain_id="d",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        with pytest.raises(ValueError, match="apply modifications"):
            grid.apply_modifications([])

    def test_apply_modifications_rederives_in_place(self, test_domain):
        # A throwaway uniform grid -- grids have no duplicate yet (#16) and the
        # shared fixture is read-only. A value-based modification (band > 0,
        # matching every cell) avoids needing a feature.
        grid = create_uniform_grid(
            test_domain,
            resolution_m=30,
            bands={"fuel_load.1hr": 0.5},
            name="grid_modify_test",
        )
        grid.wait()
        original_checksum = grid.checksum

        modification = GridModification(
            conditions=[
                GridModificationCondition(
                    band="fuel_load.1hr", operator=Operator.GT, value=0
                )
            ],
            actions=[
                GridModificationAction(
                    band="fuel_load.1hr", modifier=Modifier.MULTIPLY, value=0.9
                )
            ],
        )
        modified = grid.apply_modifications([modification])

        assert modified is grid  # in place: same object, same id
        assert modified.id == grid.id
        # The grid re-derives in place; once it settles its content has
        # changed (the multiply-by-0.9 action), so the checksum differs. (The
        # `modifications` list is not echoed in the immediate pending response,
        # unlike inventories.)
        grid.wait()
        assert grid.status == JobStatus.COMPLETED
        assert grid.checksum != original_checksum
        grid.delete()


class TestFbfm40Lookup:
    def test_lookup_returns_new_pending_grid(self, completed_fbfm40_grid):
        fuel_grid = create_fuel_grid_from_fbfm40_lookup(
            completed_fbfm40_grid,
            bands=["fuel_load.1hr", "fuel_depth"],
            name="throwaway_lookup",
        )
        assert isinstance(fuel_grid, Grid)
        assert fuel_grid.id != completed_fbfm40_grid.id
        assert fuel_grid.domain_id == completed_fbfm40_grid.domain_id
        assert fuel_grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        fuel_grid.delete()

    def test_lookup_requires_completed_source(self, test_domain):
        grid = create_fuel_model_grid_from_landfire_fbfm40(
            test_domain, output_resolution_m=30
        )
        if grid.status == JobStatus.COMPLETED:
            grid.delete()
            pytest.skip("grid completed too quickly to test the guard")
        with pytest.raises(ValueError, match="look up fuel"):
            create_fuel_grid_from_fbfm40_lookup(grid, bands=["fuel_load.1hr"])
        grid.delete()

    def test_lookup_rejects_non_fbfm_grid(self, completed_topography_grid):
        # A topography grid has no `fbfm` band; the guard rejects it before any
        # API call, naming the missing band and the right creator to use.
        with pytest.raises(ValueError, match="fbfm"):
            create_fuel_grid_from_fbfm40_lookup(
                completed_topography_grid, bands=["fuel_load.1hr"]
            )


class TestExport:
    def test_export_returns_pending_export(self, completed_topography_grid):
        # Topography is 2D, so a GeoTIFF export is valid
        export = completed_topography_grid.export(format="geotiff")
        assert len(export.id) > 0
        assert export.domain_id == completed_topography_grid.domain_id
        assert export.status in (
            JobStatus.PENDING,
            JobStatus.RUNNING,
            JobStatus.COMPLETED,
        )


class TestCheck3depCoverage:
    def test_coverage(self, test_domain):
        coverage = check_3dep_coverage(test_domain, resolution_m=10)
        # The test domain sits in CONUS, which 3DEP 10 m covers
        assert coverage.available is True
        assert coverage.tile_count >= 1


class TestListGrids:
    def test_list_in_domain(self, test_domain, completed_topography_grid):
        grid_ids = [grid.id for grid in list_grids(test_domain)]
        assert completed_topography_grid.id in grid_ids

    def test_list_cross_domain(self, completed_topography_grid):
        # No domain: list grids across all the user's domains
        grid_ids = [grid.id for grid in list_grids()]
        assert completed_topography_grid.id in grid_ids

    def test_filter_by_tag(self, test_domain, completed_topography_grid):
        grids_with_tag = list_grids(test_domain, tag="test")
        assert completed_topography_grid.id in [grid.id for grid in grids_with_tag]

    def test_invalid_sort_field(self):
        with pytest.raises(ValueError):
            list_grids(sort_by="not_a_field")


class TestToJson:
    def test_to_json(self, completed_topography_grid):
        grid_dict = json.loads(completed_topography_grid.to_json())
        assert grid_dict["id"] == completed_topography_grid.id
        assert grid_dict["domain_id"] == completed_topography_grid.domain_id


class TestDeleteGrid:
    def test_delete(self, test_domain):
        grid = create_uniform_grid(
            test_domain, resolution_m=30, bands={"fuel_depth": 0.5}
        )
        grid.delete()

        with pytest.raises(NotFoundException):
            Grid.from_id(test_domain.id, grid.id)

        with pytest.raises(NotFoundException):
            grid.delete()


class TestDuplicateGrid:
    def test_duplicate_is_a_clone(self, completed_topography_grid):
        # Duplicating creates a new grid (the shared fixture is not mutated),
        # byte-copying the data so the copy carries the same checksum.
        copy = completed_topography_grid.duplicate(name="grid_duplicate_test")
        assert copy.id != completed_topography_grid.id
        assert copy.name == "grid_duplicate_test"
        assert copy.domain_id == completed_topography_grid.domain_id
        copy.wait()
        assert copy.status == JobStatus.COMPLETED
        assert copy.checksum == completed_topography_grid.checksum
        copy.delete()


class TestDecodeGridChunk:
    """Offline unit tests for binary chunk decoding (no API required)."""

    def test_dense_c_order(self):
        values = np.arange(6, dtype=np.float32)
        offset, block = _decode_grid_chunk(
            values.tobytes(),
            {
                "X-Data-Shape": "2,3",
                "X-Data-Offset": "0,0",
                "X-Data-Order": "C",
                "X-Data-Format": "dense",
                "X-Data-Dtype": "float32",
            },
        )
        assert offset == (0, 0)
        assert block.dtype == np.float32
        assert np.array_equal(block, np.arange(6).reshape(2, 3))

    def test_dense_f_order_with_offset(self):
        values = np.arange(6, dtype=np.float32)
        offset, block = _decode_grid_chunk(
            values.tobytes(),
            {
                "X-Data-Shape": "2,3",
                "X-Data-Offset": "4,8",
                "X-Data-Order": "F",
                "X-Data-Format": "dense",
                "X-Data-Dtype": "float32",
            },
        )
        assert offset == (4, 8)
        assert np.array_equal(block, np.arange(6).reshape(2, 3, order="F"))

    def test_sparse_with_fill_value(self):
        content = (
            np.array([1], dtype=np.int32).tobytes()
            + np.array([9.0], dtype=np.float32).tobytes()
        )
        _, block = _decode_grid_chunk(
            content,
            {
                "X-Data-Shape": "2,2",
                "X-Data-Offset": "0,0",
                "X-Data-Order": "C",
                "X-Data-Format": "sparse",
                "X-Data-NNZ": "1",
                "X-Data-Index-Dtype": "int32",
                "X-Data-Value-Dtype": "float32",
                "X-Data-Fill-Value": "0",
            },
        )
        assert np.array_equal(block, np.array([[0, 9], [0, 0]], dtype=np.float32))

    def test_sparse_without_fill_uses_nan(self):
        content = (
            np.array([0, 3], dtype=np.int32).tobytes()
            + np.array([5.0, 7.0], dtype=np.float32).tobytes()
        )
        _, block = _decode_grid_chunk(
            content,
            {
                "X-Data-Shape": "2,2",
                "X-Data-Offset": "0,0",
                "X-Data-Order": "C",
                "X-Data-Format": "sparse",
                "X-Data-NNZ": "2",
                "X-Data-Index-Dtype": "int32",
                "X-Data-Value-Dtype": "float32",
            },
        )
        assert block[0, 0] == 5 and block[1, 1] == 7
        assert np.isnan(block[0, 1]) and np.isnan(block[1, 0])

    def test_fill_for(self):
        assert np.isnan(_fill_for(np.dtype("float32")))
        assert _fill_for(np.dtype("int32")) == 0
        assert _fill_for(np.dtype("float32"), -9999) == -9999
        assert _fill_for(np.dtype("int32"), UNSET) == 0


def _reassemble_band_via_json(grid, band):
    """Reassemble one band from the JSON chunk endpoint, independently of
    ``Grid.to_numpy``.

    This shares no code with the binary path: it uses the generated client's
    fully-typed JSON parser (``get_grid_data_json``) rather than hand-decoding
    raw bytes. Comparing the two arrays validates the binary decode end to end
    — dtype, byte order, sparse split, reshape order, and chunk placement.
    """
    is_3d = len(grid.georeference.shape) == 3
    array_format = GridDataArrayFormat.SPARSE if is_3d else GridDataArrayFormat.DENSE
    full = np.full(tuple(grid.georeference.shape), np.nan)
    for chunk_index in range(grid.chunks.count):
        response = expect(
            get_grid_data_json.sync_detailed(
                grid.domain_id,
                grid.id,
                band,
                chunk_index,
                client=ensure_client(),
                array_format=array_format,
                order=GridDataOrder.C,
            )
        )
        shape = response.shape
        order = response.order.value
        if response.data.format_ == "dense":
            block = np.array(response.data.values, dtype=float).reshape(
                shape, order=order
            )
        else:
            fill = response.data.fill_value
            flat = np.full(int(np.prod(shape)), np.nan if fill is None else float(fill))
            flat[np.array(response.data.indices, dtype=int)] = response.data.values
            block = flat.reshape(shape, order=order)
        slices = tuple(slice(o, o + s) for o, s in zip(response.metadata.offset, shape))
        full[slices] = block
    return full


class TestDataOut:
    """Live tests for reading grid data into memory."""

    def test_to_numpy_topography(self, completed_topography_grid):
        grid = completed_topography_grid
        array = grid.to_numpy(grid.bands[0].key)
        assert array.shape == tuple(grid.georeference.shape)
        assert array.ndim == len(grid.georeference.shape)
        assert np.isfinite(array).any()

    def test_to_numpy_matches_json_transport(self, completed_topography_grid):
        # The binary reconstruction must agree, value for value, with an
        # independent reassembly over the JSON chunk endpoint.
        grid = completed_topography_grid
        band = grid.bands[0].key
        binary = grid.to_numpy(band)
        reference = _reassemble_band_via_json(grid, band)
        assert binary.shape == reference.shape
        assert np.allclose(binary, reference, equal_nan=True)

    def test_topography_values_are_plausible(self, completed_topography_grid):
        # Guards against all-zero / constant-fill / garbage decodes that a
        # shape-only check would miss: real terrain varies and sits within
        # Earth's elevation range (meters).
        grid = completed_topography_grid
        elevation = grid.to_numpy("elevation")
        finite = elevation[np.isfinite(elevation)]
        assert finite.size > 0
        assert finite.std() > 0
        assert -500 < finite.min() and finite.max() < 9000

    def test_to_numpy_pim(self, completed_pim_grid):
        # Exercises whichever encoding the PIM grid uses (3D -> sparse).
        grid = completed_pim_grid
        array = grid.to_numpy(grid.bands[0].key)
        assert array.shape == tuple(grid.georeference.shape)

    def test_to_numpy_unknown_band(self, completed_topography_grid):
        with pytest.raises(ValueError):
            completed_topography_grid.to_numpy("not_a_band")

    def test_to_numpy_requires_completed(self, test_domain):
        grid = create_topography_grid_from_3dep(test_domain, output_resolution_m=10)
        try:
            with pytest.raises(ValueError):
                grid.to_numpy("elevation")
        finally:
            grid.delete()

    def test_to_xarray(self, completed_topography_grid):
        grid = completed_topography_grid
        dataset = grid.to_xarray()
        assert set(dataset.data_vars) == {band.key for band in grid.bands}
        assert dataset.sizes["x"] == grid.georeference.shape[-1]
        assert dataset.sizes["y"] == grid.georeference.shape[-2]
        assert dataset.attrs["crs"] == grid.georeference.crs
