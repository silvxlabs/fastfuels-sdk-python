"""
tests/v2/test_grids.py
"""

# Core imports
import inspect
import json
from types import SimpleNamespace
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2 import grids
from fastfuels_sdk.v2.grids import (
    Grid,
    _build_alignment,
    _domain_id,
    _enum_list,
    _opt,
    check_3dep_coverage,
    create_canopy_fuel_grid_from_landfire,
    create_canopy_height_grid_from_meta,
    create_canopy_height_grid_from_naip_chm,
    create_fuel_model_grid_from_landfire_fbfm40,
    create_fuel_model_grid_from_landfire_fccs,
    create_pim_grid_from_treemap,
    create_topography_grid_from_3dep,
    create_topography_grid_from_landfire,
    create_uniform_grid,
    get_grid,
    list_grids,
)
from fastfuels_sdk.v2.client_library.models import (
    GridAlignmentDomainTarget,
    GridAlignmentGridTarget,
    GridAlignmentNativeTarget,
    JobStatus,
    ResamplingMethod,
    TopographyBand,
)
from fastfuels_sdk.v2.client_library.types import UNSET
from fastfuels_sdk.v2.exceptions import NotFoundException

# External imports
import pytest

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
    """The FCCS request model has no alignment field, so the SDK creator
    exposes no alignment kwargs (unlike the other LANDFIRE creators)."""

    def test_fccs_has_no_alignment_kwargs(self):
        params = inspect.signature(
            grids.create_fuel_model_grid_from_landfire_fccs
        ).parameters
        for forbidden in (
            "output_resolution_m",
            "align_to",
            "align",
            "resampling",
            "extent_buffer_cells",
        ):
            assert forbidden not in params

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


class TestCreateFuelModelGridFromLandfireFccs:
    def test_create(self, test_domain):
        # FCCS is alignment-free; only metadata and remove_bare_ground apply
        grid = create_fuel_model_grid_from_landfire_fccs(
            test_domain, remove_bare_ground=True, name="throwaway_fccs"
        )
        assert len(grid.id) > 0
        assert grid.domain_id == test_domain.id
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
    matches the domain CRS. There is no committed raster fixture and no
    raster dependency (rasterio/xarray) in the test environment to build
    one on the fly, so these paths are deferred rather than mocked.
    """

    @pytest.mark.skip(
        reason="needs a committed GeoTIFF fixture matching the domain CRS"
    )
    def test_create_grid_from_geotiff(self, test_domain):
        pass

    @pytest.mark.skip(reason="needs a committed NetCDF fixture matching the domain CRS")
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


class TestLookupFuelModelValues:
    def test_lookup_returns_new_pending_grid(self, completed_fbfm40_grid):
        fuel_grid = completed_fbfm40_grid.lookup_fuel_model_values(
            bands=["fuel_load.1hr", "fuel_depth"], name="throwaway_lookup"
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
            grid.lookup_fuel_model_values(bands=["fuel_load.1hr"])
        grid.delete()


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
