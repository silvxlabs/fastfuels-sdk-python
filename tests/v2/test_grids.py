"""
tests/v2/test_grids.py
"""

# Core imports
import datetime
import inspect
import json
import math
from http import HTTPStatus
from types import SimpleNamespace
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2 import grids
from fastfuels_sdk.v2.calibrations import duet_calibration
from fastfuels_sdk.v2.grids import (
    Grid,
    _build_alignment,
    _build_chm_aggregation,
    _build_chm_spike_filter,
    _decode_grid_chunk,
    _domain_id,
    _enum_list,
    _fill_for,
    _opt,
    check_3dep_coverage,
    create_canopy_fuel_grid_from_inventory,
    create_canopy_fuel_grid_from_landfire,
    create_canopy_height_grid_from_meta,
    create_canopy_height_grid_from_naip_chm,
    create_canopy_height_grid_from_point_cloud,
    create_dead_fuel_moisture_grid_from_fosberg,
    create_fuel_grid_from_fccs_lookup,
    create_fuel_grid_from_fbfm13_lookup,
    create_fuel_grid_from_fbfm40_lookup,
    create_fuel_model_grid_from_landfire_fbfm13,
    create_fuel_model_grid_from_landfire_fbfm40,
    create_fuel_model_grid_from_landfire_fccs,
    create_grid_from_geotiff,
    create_irradiance_grid_from_leaflux,
    create_pim_grid_from_treemap,
    create_surface_fuel_grid_from_duet,
    create_topography_grid_from_3dep,
    create_topography_grid_from_landfire,
    create_uniform_grid,
    get_grid,
    list_grids,
)
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.domains import Domain
from fastfuels_sdk.v2.point_clouds import (
    create_point_cloud_from_3dep,
    check_3dep_coverage as check_3dep_point_cloud_coverage,
)
from fastfuels_sdk.v2.client_library.api.grids import get_grid_data_json
from fastfuels_sdk.v2.client_library.models import (
    Band,
    BandType,
    CanopyCbhPercentile,
    ChmMaxAggregation,
    ChmMeanAggregation,
    ChmMedianAggregation,
    ChmPercentileAggregation,
    ChmSpikeFilter,
    ContinuousBandSummary,
    DuetBand,
    InventoryCanopyBand,
    InventoryColumnCanopyBiomassSource,
    FccsLookupBand,
    Fbfm13LookupBand,
    FuelMoistureMonth,
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
    LeafluxBand,
    Modifier,
    Operator,
    PointCloudType,
    RelativeElevation,
    ResamplingMethod,
    TopographyBand,
    UploadBandDefinition,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Response
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    expect,
)
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


@pytest.fixture(scope="module")
def covered_3dep_point_cloud():
    """A completed ALS point cloud over a Bondurant, WY domain with stable
    3DEP LiDAR coverage. Owns its own domain so the live CHM test can build
    grids inside it without touching the shared session domain.
    """
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
        name="test_point_cloud_chm_domain",
        tags=["sdk-test"],
    )
    coverage = check_3dep_point_cloud_coverage(domain)
    point_cloud = create_point_cloud_from_3dep(
        domain,
        datasets=[coverage.datasets[0].name],
        name="test_point_cloud_chm_source",
        tags=["sdk-test"],
    )
    point_cloud.wait()
    yield point_cloud
    domain.delete(force=True)


class TestCreateCanopyHeightGridFromPointCloud:
    @staticmethod
    def _point_cloud(status=JobStatus.COMPLETED, type_=PointCloudType.ALS):
        return SimpleNamespace(
            id="pc-id",
            domain_id="domain-id",
            status=status,
            type_=type_,
        )

    def test_builds_request_from_completed_als_cloud(self, monkeypatch):
        created = Grid(
            id="grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[Band(key="chm", type_=BandType.CONTINUOUS, index=0, unit="m")],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_point_cloud_chm,
            "sync_detailed",
            fake_create,
        )

        grid = create_canopy_height_grid_from_point_cloud(
            self._point_cloud(),
            output_resolution_m=2,
            name="Point-cloud CHM",
        )

        assert isinstance(grid, Grid)
        assert grid.id == "grid-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert captured["body"].source_point_cloud_id == "pc-id"
        assert captured["body"].alignment.resolution == 2
        assert captured["body"].name == "Point-cloud CHM"

    def test_requires_completed_cloud(self):
        with pytest.raises(ValueError, match="must be completed"):
            create_canopy_height_grid_from_point_cloud(
                self._point_cloud(status=JobStatus.PENDING)
            )

    def test_requires_airborne_cloud(self):
        with pytest.raises(ValueError, match="airborne"):
            create_canopy_height_grid_from_point_cloud(
                self._point_cloud(type_=PointCloudType.TLS)
            )

    def _capture_body(self, monkeypatch, **kwargs):
        created = Grid(
            id="grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[Band(key="chm", type_=BandType.CONTINUOUS, index=0, unit="m")],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        monkeypatch.setattr(grids, "ensure_client", lambda: object())
        monkeypatch.setattr(grids.create_point_cloud_chm, "sync_detailed", fake_create)
        create_canopy_height_grid_from_point_cloud(self._point_cloud(), **kwargs)
        return captured["body"]

    def test_defaults_leave_aggregation_and_spike_filter_unset(self, monkeypatch):
        body = self._capture_body(monkeypatch)
        assert body.aggregation is UNSET
        assert body.spike_filter is UNSET

    def test_percentile_aggregation_in_request(self, monkeypatch):
        body = self._capture_body(monkeypatch, aggregation="percentile", percentile=95)
        assert isinstance(body.aggregation, ChmPercentileAggregation)
        assert body.aggregation.percentile == 95

    def test_spike_filter_thresholds_in_request(self, monkeypatch):
        body = self._capture_body(
            monkeypatch,
            spike_filter={"min_canopy_footprint_m": 5, "min_prominence_m": 30},
        )
        assert isinstance(body.spike_filter, ChmSpikeFilter)
        assert body.spike_filter.min_canopy_footprint_m == 5
        assert body.spike_filter.min_prominence_m == 30

    def test_spike_filter_false_disables(self, monkeypatch):
        body = self._capture_body(monkeypatch, spike_filter=False)
        assert body.spike_filter is None

    def test_create_live(self, covered_3dep_point_cloud):
        grid = None
        try:
            grid = create_canopy_height_grid_from_point_cloud(
                covered_3dep_point_cloud,
                output_resolution_m=2,
                aggregation="percentile",
                percentile=95,
                spike_filter={"min_canopy_footprint_m": 5, "min_prominence_m": 30},
                name="test_point_cloud_chm",
                tags=["sdk-test"],
            )
            grid.wait()
            assert grid.status == JobStatus.COMPLETED
            assert {band.key for band in grid.bands} == {"chm"}
            heights = grid.to_numpy("chm")
            assert heights.ndim == 2
            assert np.isfinite(heights).any()
        finally:
            if grid is not None:
                grid.delete()


class TestBuildChmAggregation:
    def test_none_is_unset(self):
        assert _build_chm_aggregation(None, None) is UNSET

    def test_max_mean_median(self):
        assert isinstance(_build_chm_aggregation("max", None), ChmMaxAggregation)
        assert isinstance(_build_chm_aggregation("mean", None), ChmMeanAggregation)
        assert isinstance(_build_chm_aggregation("median", None), ChmMedianAggregation)

    def test_percentile_carries_value(self):
        agg = _build_chm_aggregation("percentile", 90)
        assert isinstance(agg, ChmPercentileAggregation)
        assert agg.percentile == 90

    def test_percentile_requires_value(self):
        with pytest.raises(ValueError, match="requires a percentile"):
            _build_chm_aggregation("percentile", None)

    def test_percentile_only_with_percentile_method(self):
        with pytest.raises(ValueError, match="only used with"):
            _build_chm_aggregation("max", 90)
        with pytest.raises(ValueError, match="only used with"):
            _build_chm_aggregation(None, 90)

    def test_unknown_method_raises(self):
        with pytest.raises(ValueError, match="aggregation must be one of"):
            _build_chm_aggregation("mode", None)


class TestBuildChmSpikeFilter:
    def test_none_is_unset(self):
        assert _build_chm_spike_filter(None) is UNSET

    def test_false_disables(self):
        assert _build_chm_spike_filter(False) is None

    def test_true_is_default_filter(self):
        assert isinstance(_build_chm_spike_filter(True), ChmSpikeFilter)

    def test_mapping_sets_fields(self):
        sf = _build_chm_spike_filter({"min_prominence_m": 40})
        assert isinstance(sf, ChmSpikeFilter)
        assert sf.min_prominence_m == 40

    def test_instance_passes_through(self):
        sf = ChmSpikeFilter(min_canopy_footprint_m=4)
        assert _build_chm_spike_filter(sf) is sf

    def test_invalid_raises(self):
        with pytest.raises(ValueError, match="spike_filter must be"):
            _build_chm_spike_filter("aggressive")


class TestCreateSurfaceFuelGridFromDuet:
    @staticmethod
    def _source_grid(
        status=JobStatus.COMPLETED,
        omit=None,
    ):
        required = [
            ("bulk_density.foliage.live", BandType.CONTINUOUS),
            ("spcd", BandType.CATEGORICAL),
            ("fuel_moisture.live", BandType.CONTINUOUS),
        ]
        return Grid(
            id="tree-grid-id",
            domain_id="domain-id",
            status=status,
            source=GridSource(),
            bands=[
                Band(key=key, type_=type_, index=index)
                for index, (key, type_) in enumerate(required)
                if key != omit
            ],
        )

    def test_builds_request_from_completed_tree_grid(self, monkeypatch):
        created = Grid(
            id="duet-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        calibration = duet_calibration(fuel_load={"grass": {"mean": 0.5, "sd": 0.25}})
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_duet_grid,
            "sync_detailed",
            fake_create,
        )

        grid = create_surface_fuel_grid_from_duet(
            self._source_grid(),
            years_since_burn=20,
            wind_direction=225,
            wind_variability=45,
            bands=["fuel_load.grass", DuetBand.FUEL_LOAD_LITTER],
            calibration=calibration,
            name="DUET surface fuels",
            tags=["test"],
        )

        assert grid.id == "duet-grid-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert captured["body"].source_grid_id == "tree-grid-id"
        assert captured["body"].years_since_burn == 20
        assert captured["body"].wind_direction == 225
        assert captured["body"].wind_variability == 45
        assert captured["body"].bands == [
            DuetBand.FUEL_LOAD_GRASS,
            DuetBand.FUEL_LOAD_LITTER,
        ]
        assert captured["body"].calibration is calibration
        assert captured["body"].name == "DUET surface fuels"
        assert captured["body"].tags == ["test"]

    def test_requires_completed_tree_grid(self):
        with pytest.raises(ValueError, match=r"Call \.wait\(\)"):
            create_surface_fuel_grid_from_duet(
                self._source_grid(status=JobStatus.PENDING),
                years_since_burn=20,
            )

    def test_requires_duet_source_bands(self):
        with pytest.raises(ValueError, match="fuel_moisture.live"):
            create_surface_fuel_grid_from_duet(
                self._source_grid(omit="fuel_moisture.live"),
                years_since_burn=20,
            )

    @pytest.mark.parametrize(
        "kwargs,error",
        [
            ({"years_since_burn": 0}, ValueError),
            ({"years_since_burn": 101}, ValueError),
            ({"years_since_burn": 1.5}, TypeError),
            ({"years_since_burn": 20, "wind_direction": 360}, ValueError),
            ({"years_since_burn": 20, "wind_variability": 181}, ValueError),
            ({"years_since_burn": 20, "bands": []}, ValueError),
            (
                {
                    "years_since_burn": 20,
                    "bands": ["fuel_load.grass", "fuel_load.grass"],
                },
                ValueError,
            ),
        ],
    )
    def test_validates_request_parameters(self, kwargs, error):
        with pytest.raises(error):
            create_surface_fuel_grid_from_duet(self._source_grid(), **kwargs)

    def test_create_live(self, completed_tree_inventory):
        voxels = completed_tree_inventory.voxelize(
            horizontal_resolution_m=2,
            vertical_resolution_m=1,
            bands=[
                "bulk_density.foliage.live",
                "spcd",
                "fuel_moisture.live",
            ],
            name="test_duet_source",
            tags=["test"],
        )
        surface = None
        try:
            voxels.wait()
            surface = create_surface_fuel_grid_from_duet(
                voxels,
                years_since_burn=25,
                bands=[
                    "fuel_load.grass",
                    "fuel_load.litter",
                    "fuel_depth.grass",
                    "fuel_depth.litter",
                ],
                calibration=duet_calibration(
                    fuel_load={
                        "grass": {"mean": 0.5, "sd": 0.25},
                        "litter": {"max": 5, "min": 0},
                    },
                    fuel_depth={
                        "grass": {"value": 0.3},
                        "litter": {"value": 0.06},
                    },
                ),
                name="test_duet_surface_fuels",
                tags=["test"],
            )
            surface.wait()
            assert surface.status == JobStatus.COMPLETED
            assert {band.key for band in surface.bands} == {
                "fuel_load.grass",
                "fuel_load.litter",
                "fuel_depth.grass",
                "fuel_depth.litter",
            }
            grass_load = surface.to_numpy("fuel_load.grass")
            assert grass_load.ndim == 2
            assert np.isfinite(grass_load).any()
        finally:
            if surface is not None:
                surface.delete()
            voxels.delete()


class TestCreateDeadFuelMoistureGridFromFosberg:
    @staticmethod
    def _topo_grid(status=JobStatus.COMPLETED, omit=None):
        bands = [
            ("slope", BandType.CONTINUOUS),
            ("aspect", BandType.CONTINUOUS),
        ]
        return Grid(
            id="topo-grid-id",
            domain_id="domain-id",
            status=status,
            source=GridSource(),
            bands=[
                Band(key=key, type_=type_, index=index)
                for index, (key, type_) in enumerate(bands)
                if key != omit
            ],
        )

    @staticmethod
    def _irradiance_grid(status=JobStatus.COMPLETED, omit=None):
        bands = [("irradiance.surface.relative", BandType.CONTINUOUS)]
        return Grid(
            id="irradiance-grid-id",
            domain_id="domain-id",
            status=status,
            source=GridSource(),
            bands=[
                Band(key=key, type_=type_, index=index)
                for index, (key, type_) in enumerate(bands)
                if key != omit
            ],
        )

    def _patch_endpoint(self, monkeypatch):
        created = Grid(
            id="fosberg-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_fosberg_fuel_moisture_grid,
            "sync_detailed",
            fake_create,
        )
        return captured, client

    def test_builds_request_from_completed_grids(self, monkeypatch):
        captured, client = self._patch_endpoint(monkeypatch)

        grid = create_dead_fuel_moisture_grid_from_fosberg(
            self._topo_grid(),
            self._irradiance_grid(),
            dry_bulb_temp=75.0,
            relative_humidity=20.0,
            time=1200,
            month="July",
            elevation="near",
            name="Fosberg moisture",
            tags=["test"],
        )

        assert grid.id == "fosberg-grid-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        body = captured["body"]
        assert body.source_topography_grid_id == "topo-grid-id"
        assert body.source_irradiance_grid_id == "irradiance-grid-id"
        assert body.dry_bulb_temp == 75.0
        assert body.relative_humidity == 20.0
        assert body.time == 1200
        assert body.month == FuelMoistureMonth.JULY
        assert body.elevation == RelativeElevation.NEAR
        assert body.name == "Fosberg moisture"
        assert body.tags == ["test"]

    def test_elevation_defaults_to_unset(self, monkeypatch):
        captured, _ = self._patch_endpoint(monkeypatch)

        create_dead_fuel_moisture_grid_from_fosberg(
            self._topo_grid(),
            self._irradiance_grid(),
            dry_bulb_temp=75.0,
            relative_humidity=20.0,
            time=1200,
            month=FuelMoistureMonth.AUGUST,
        )

        assert captured["body"].elevation is UNSET

    def test_accepts_grid_ids_with_one_object(self, monkeypatch):
        # Irradiance passed as a bare id; the domain is resolved from the
        # topography Grid object.
        captured, _ = self._patch_endpoint(monkeypatch)

        create_dead_fuel_moisture_grid_from_fosberg(
            self._topo_grid(),
            "some-irradiance-id",
            dry_bulb_temp=75.0,
            relative_humidity=20.0,
            time=1200,
            month="July",
        )

        assert captured["domain_id"] == "domain-id"
        assert captured["body"].source_irradiance_grid_id == "some-irradiance-id"

    def test_requires_domain_when_both_ids(self, monkeypatch):
        self._patch_endpoint(monkeypatch)
        with pytest.raises(ValueError, match="resolve the domain"):
            create_dead_fuel_moisture_grid_from_fosberg(
                "topo-id",
                "irradiance-id",
                dry_bulb_temp=75.0,
                relative_humidity=20.0,
                time=1200,
                month="July",
            )

    def test_requires_completed_topography_grid(self):
        with pytest.raises(ValueError, match=r"Call \.wait\(\)"):
            create_dead_fuel_moisture_grid_from_fosberg(
                self._topo_grid(status=JobStatus.PENDING),
                self._irradiance_grid(),
                dry_bulb_temp=75.0,
                relative_humidity=20.0,
                time=1200,
                month="July",
            )

    def test_requires_completed_irradiance_grid(self):
        with pytest.raises(ValueError, match=r"Call \.wait\(\)"):
            create_dead_fuel_moisture_grid_from_fosberg(
                self._topo_grid(),
                self._irradiance_grid(status=JobStatus.PENDING),
                dry_bulb_temp=75.0,
                relative_humidity=20.0,
                time=1200,
                month="July",
            )

    def test_requires_topography_bands(self):
        with pytest.raises(ValueError, match="aspect"):
            create_dead_fuel_moisture_grid_from_fosberg(
                self._topo_grid(omit="aspect"),
                self._irradiance_grid(),
                dry_bulb_temp=75.0,
                relative_humidity=20.0,
                time=1200,
                month="July",
            )

    def test_requires_irradiance_band(self):
        with pytest.raises(ValueError, match="irradiance.surface.relative"):
            create_dead_fuel_moisture_grid_from_fosberg(
                self._topo_grid(),
                self._irradiance_grid(omit="irradiance.surface.relative"),
                dry_bulb_temp=75.0,
                relative_humidity=20.0,
                time=1200,
                month="July",
            )

    @pytest.mark.parametrize(
        "kwargs,error",
        [
            ({"dry_bulb_temp": 9}, ValueError),
            ({"dry_bulb_temp": "hot"}, TypeError),
            ({"relative_humidity": -1}, ValueError),
            ({"relative_humidity": 101}, ValueError),
            ({"time": 759}, ValueError),
            ({"time": 2000}, ValueError),
            ({"time": 1275}, ValueError),
            ({"time": 12.0}, TypeError),
        ],
    )
    def test_validates_request_parameters(self, kwargs, error):
        params = dict(
            dry_bulb_temp=75.0,
            relative_humidity=20.0,
            time=1200,
            month="July",
        )
        params.update(kwargs)
        with pytest.raises(error):
            create_dead_fuel_moisture_grid_from_fosberg(
                self._topo_grid(),
                self._irradiance_grid(),
                **params,
            )

    def test_create_live(self, completed_tree_inventory):
        voxels = completed_tree_inventory.voxelize(
            horizontal_resolution_m=2,
            vertical_resolution_m=1,
            bands=["leaf_area_density"],
            name="test_fosberg_lad",
            tags=["test"],
        )
        topo = None
        irradiance = None
        moisture = None
        try:
            voxels.wait()
            # Surface irradiance and the Fosberg model require the topography,
            # LAD, and irradiance grids to share one horizontal lattice, so
            # align the topography grid to the voxelized LAD grid.
            # elevation feeds the leaflux surface draping; slope + aspect feed
            # the Fosberg model.
            topo = create_topography_grid_from_3dep(
                completed_tree_inventory.domain_id,
                align_to=voxels,
                bands=["elevation", "slope", "aspect"],
                name="test_fosberg_topo",
                tags=["test"],
            )
            topo.wait()
            irradiance = create_irradiance_grid_from_leaflux(
                voxels,
                date_time=datetime.datetime(
                    2020, 7, 1, 18, 0, tzinfo=datetime.timezone.utc
                ),
                source_terrain_grid=topo,
                bands=["irradiance.surface.relative"],
                name="test_fosberg_irradiance",
                tags=["test"],
            )
            irradiance.wait()
            moisture = create_dead_fuel_moisture_grid_from_fosberg(
                topo,
                irradiance,
                dry_bulb_temp=75.0,
                relative_humidity=20.0,
                time=1200,
                month="July",
                elevation="near",
                name="test_fosberg_moisture",
                tags=["test"],
            )
            moisture.wait()
            assert moisture.status == JobStatus.COMPLETED
            assert {band.key for band in moisture.bands} == {"fuel_moisture.dead.1hr"}
            values = moisture.to_numpy("fuel_moisture.dead.1hr")
            assert values.ndim == 2
            assert np.isfinite(values).any()
        finally:
            if moisture is not None:
                moisture.delete()
            if irradiance is not None:
                irradiance.delete()
            if topo is not None:
                topo.delete()
            voxels.delete()


class TestCreateCanopyFuelGridFromInventory:
    @staticmethod
    def _inventory(status=JobStatus.COMPLETED):
        return SimpleNamespace(id="inv-id", domain_id="domain-id", status=status)

    def _patch_create(self, monkeypatch):
        """Patch the endpoint to capture the request body and return a Grid."""
        created = Grid(
            id="canopy-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_inventory_canopy_grid, "sync_detailed", fake_create
        )
        return captured

    def test_builds_request_from_inventory_object(self, monkeypatch):
        captured = self._patch_create(monkeypatch)

        grid = create_canopy_fuel_grid_from_inventory(
            self._inventory(),
            bands=["cbd", InventoryCanopyBand.CFL],
            biomass_equations="nsvb",
            species_inclusion="fuelcalc_default",
            crown_class_adjustment="fuelcalc_table",
            min_tree_height=1.83,
            vertical_distribution="uniform",
            horizontal_distribution="stem",
            max_crown_radius_equations="crookston_stage",
            cbd="running_mean",
            cbh="minimum",
            chm="threshold",
            cc="crown_union",
            output_resolution_m=30,
            name="canopy",
            tags=["test"],
        )

        assert grid.id == "canopy-grid-id"
        assert captured["domain_id"] == "domain-id"
        body = captured["body"]
        assert body.source_inventory_id == "inv-id"
        assert body.bands == [InventoryCanopyBand.CBD, InventoryCanopyBand.CFL]
        assert body.biomass_source.equations.value == "nsvb"
        assert body.species_inclusion.value == "fuelcalc_default"
        assert body.crown_class_adjustment.method == "fuelcalc_table"
        assert body.min_tree_height == 1.83
        assert body.vertical_distribution.value == "uniform"
        assert body.horizontal_distribution.value == "stem"
        assert body.max_crown_radius_source.equations.value == "crookston_stage"
        assert body.cbd.method == "maximum_running_mean"
        assert body.cbh.method == "minimum"
        assert body.chm.method == "bulk_density_threshold"
        assert body.cc.method == "crown_union"
        assert body.alignment.resolution == 30
        assert body.name == "canopy"
        assert body.tags == ["test"]

    def test_inventory_column_biomass_source(self, monkeypatch):
        captured = self._patch_create(monkeypatch)

        create_canopy_fuel_grid_from_inventory(
            self._inventory(), biomass_column="available_canopy_fuel"
        )

        body = captured["body"]
        assert isinstance(body.biomass_source, InventoryColumnCanopyBiomassSource)
        assert body.biomass_source.column == "available_canopy_fuel"

    def test_available_fuel_from_kwargs(self, monkeypatch):
        captured = self._patch_create(monkeypatch)

        create_canopy_fuel_grid_from_inventory(
            self._inventory(),
            foliage_fraction=0.9,
            branchwood_fraction=0.5,
            branchwood_size_partition="equations",
        )

        available_fuel = captured["body"].available_fuel
        assert available_fuel.foliage_fraction == 0.9
        assert available_fuel.branchwood.fraction == 0.5
        assert available_fuel.branchwood.size_partition.value == "equations"

    def test_method_objects_passed_through(self, monkeypatch):
        captured = self._patch_create(monkeypatch)

        percentile = CanopyCbhPercentile(percentile=25)
        create_canopy_fuel_grid_from_inventory(self._inventory(), cbh=percentile)

        assert captured["body"].cbh is percentile

    def test_defaults_are_unset(self, monkeypatch):
        captured = self._patch_create(monkeypatch)

        create_canopy_fuel_grid_from_inventory(self._inventory())

        body = captured["body"]
        assert body.biomass_source is UNSET
        assert body.available_fuel is UNSET
        assert body.cbd is UNSET
        assert body.bands is UNSET
        assert body.alignment is UNSET

    def test_bare_id_without_domain_raises(self):
        with pytest.raises(ValueError, match="Inventory object"):
            create_canopy_fuel_grid_from_inventory("inv-id")

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"biomass_equations": "nsvb", "biomass_column": "col"},
            {
                "max_crown_radius_equations": "purves",
                "max_crown_radius_column": "col",
            },
            {"crown_class_adjustment": "bogus"},
            {"cbh": "bogus_method"},
            {"cbh": "percentile"},
        ],
    )
    def test_invalid_kwargs_raise(self, kwargs):
        with pytest.raises(ValueError):
            create_canopy_fuel_grid_from_inventory(self._inventory(), **kwargs)

    def test_create_live(self, completed_tree_inventory):
        canopy = create_canopy_fuel_grid_from_inventory(
            completed_tree_inventory,
            bands=["cbd", "cbh", "chm", "cc", "cfl"],
            output_resolution_m=30,
            name="test_inventory_canopy",
            tags=["test"],
        )
        try:
            canopy.wait()
            assert canopy.status == JobStatus.COMPLETED
            assert {band.key for band in canopy.bands} == {
                "cbd",
                "cbh",
                "chm",
                "cc",
                "cfl",
            }
            cbd = canopy.to_numpy("cbd")
            assert cbd.ndim == 2
            assert np.isfinite(cbd).any()
        finally:
            canopy.delete()


class TestCreateIrradianceGridFromLeaflux:
    @staticmethod
    def _source_grid(status=JobStatus.COMPLETED, omit=False):
        bands = (
            []
            if omit
            else [Band(key="leaf_area_density", type_=BandType.CONTINUOUS, index=0)]
        )
        return Grid(
            id="lad-grid-id",
            domain_id="domain-id",
            status=status,
            source=GridSource(),
            bands=bands,
        )

    @staticmethod
    def _patch(monkeypatch, captured):
        created = Grid(
            id="irradiance-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_leaflux_irradiance_grid,
            "sync_detailed",
            fake_create,
        )
        return client

    def test_builds_request_from_completed_grid(self, monkeypatch):
        captured = {}
        client = self._patch(monkeypatch, captured)
        when = datetime.datetime(2024, 7, 1, 18, 30, tzinfo=datetime.timezone.utc)

        grid = create_irradiance_grid_from_leaflux(
            self._source_grid(),
            date_time=when,
            source_terrain_grid="terrain-grid-id",
            bands=[
                "irradiance.canopy.relative",
                LeafluxBand.IRRADIANCE_SURFACE_RELATIVE,
            ],
            extinction_coefficient=0.7,
            name="leaflux irradiance",
            tags=["test"],
        )

        assert grid.id == "irradiance-grid-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert captured["body"].source_lad_grid_id == "lad-grid-id"
        assert captured["body"].date_time == when
        assert captured["body"].source_terrain_grid_id == "terrain-grid-id"
        assert captured["body"].bands == [
            LeafluxBand.IRRADIANCE_CANOPY_RELATIVE,
            LeafluxBand.IRRADIANCE_SURFACE_RELATIVE,
        ]
        assert captured["body"].extinction_coefficient == 0.7
        assert captured["body"].name == "leaflux irradiance"
        assert captured["body"].tags == ["test"]

    def test_defaults_leave_bands_and_terrain_unset(self, monkeypatch):
        captured = {}
        self._patch(monkeypatch, captured)

        create_irradiance_grid_from_leaflux(
            self._source_grid(),
            date_time=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
        )

        assert captured["body"].bands is UNSET
        assert captured["body"].source_terrain_grid_id is UNSET
        assert captured["body"].extinction_coefficient == 0.5

    def test_accepts_ids_with_explicit_domain(self, monkeypatch):
        captured = {}
        self._patch(monkeypatch, captured)

        create_irradiance_grid_from_leaflux(
            "lad-grid-id",
            date_time=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            source_terrain_grid=SimpleNamespace(id="terrain-grid-id"),
            domain=SimpleNamespace(id="domain-id"),
        )

        assert captured["domain_id"] == "domain-id"
        assert captured["body"].source_lad_grid_id == "lad-grid-id"
        assert captured["body"].source_terrain_grid_id == "terrain-grid-id"

    def test_requires_domain_for_id_source(self):
        with pytest.raises(ValueError, match="domain="):
            create_irradiance_grid_from_leaflux(
                "lad-grid-id",
                date_time=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            )

    def test_requires_completed_source_grid(self):
        with pytest.raises(ValueError, match=r"Call \.wait\(\)"):
            create_irradiance_grid_from_leaflux(
                self._source_grid(status=JobStatus.PENDING),
                date_time=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            )

    def test_requires_leaf_area_density_band(self):
        with pytest.raises(ValueError, match="leaf_area_density"):
            create_irradiance_grid_from_leaflux(
                self._source_grid(omit=True),
                date_time=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            )

    def test_create_live(self, completed_tree_inventory):
        voxels = completed_tree_inventory.voxelize(
            horizontal_resolution_m=2,
            vertical_resolution_m=1,
            bands=["leaf_area_density"],
            name="test_leaflux_source",
            tags=["test"],
        )
        irradiance = None
        try:
            voxels.wait()
            irradiance = create_irradiance_grid_from_leaflux(
                voxels,
                date_time=datetime.datetime(
                    2024, 7, 1, 18, 0, tzinfo=datetime.timezone.utc
                ),
                bands=["irradiance.canopy.relative"],
                name="test_leaflux_irradiance",
                tags=["test"],
            )
            irradiance.wait()
            assert irradiance.status == JobStatus.COMPLETED
            assert "irradiance.canopy.relative" in {
                band.key for band in irradiance.bands
            }
            values = irradiance.to_numpy("irradiance.canopy.relative")
            assert values.ndim == 3
            assert np.isfinite(values).any()
        finally:
            if irradiance is not None:
                irradiance.delete()
            voxels.delete()


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

    def test_create_new_version_reports_year(self, test_domain):
        # Annual FBFM40's represented year is its version, populated on the
        # source the moment the pending grid is returned.
        grid = create_fuel_model_grid_from_landfire_fbfm40(
            test_domain,
            version="2024",
            output_resolution_m=30,
            name="throwaway_fbfm40_2024",
        )
        assert grid.represented_year == 2024
        grid.delete()

    @pytest.mark.parametrize("version", ["2024", "2025"])
    def test_builds_request_accepts_new_versions(self, monkeypatch, version):
        created = Grid(
            id="fbfm40-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_landfire_fbfm40,
            "sync_detailed",
            fake_create,
        )

        create_fuel_model_grid_from_landfire_fbfm40(
            SimpleNamespace(id="domain-id"),
            version=version,
            output_resolution_m=30,
        )

        assert captured["body"].version.value == version

    def test_rejects_unknown_version(self):
        with pytest.raises(ValueError):
            create_fuel_model_grid_from_landfire_fbfm40(
                SimpleNamespace(id="domain-id"),
                version="1999",
            )


class TestRepresentedYear:
    """Unit tests for the Grid.represented_year accessor (no API)."""

    def test_reads_year_from_source(self):
        source = GridSource()
        source["year"] = 2026
        grid = Grid(
            id="grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=source,
            bands=[],
        )
        assert grid.represented_year == 2026

    def test_none_when_source_has_no_year(self):
        grid = Grid(
            id="grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        assert grid.represented_year is None


class TestCreateFuelModelGridFromLandfireFbfm13:
    def test_builds_request(self, monkeypatch):
        created = Grid(
            id="fbfm13-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_landfire_fbfm13,
            "sync_detailed",
            fake_create,
        )

        grid = create_fuel_model_grid_from_landfire_fbfm13(
            SimpleNamespace(id="domain-id"),
            version="2024",
            remove_non_burnable=["NB1", "NB2"],
            output_resolution_m=30,
            name="Anderson 13",
        )

        assert grid.id == "fbfm13-grid-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert captured["body"].version.value == "2024"
        assert [value.value for value in captured["body"].remove_non_burnable] == [
            "NB1",
            "NB2",
        ]
        assert captured["body"].alignment.resolution == 30
        assert captured["body"].name == "Anderson 13"

    def test_completed_fixture(self, completed_fbfm13_grid):
        assert completed_fbfm13_grid.status == JobStatus.COMPLETED
        assert [band.key for band in completed_fbfm13_grid.bands] == ["fbfm13"]


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


class TestFbfm13Lookup:
    @staticmethod
    def _source(status=JobStatus.COMPLETED, band="fbfm13"):
        return Grid(
            id="fbfm13-grid-id",
            domain_id="domain-id",
            status=status,
            source=GridSource(),
            bands=[Band(key=band, type_=BandType.CATEGORICAL, index=0)],
        )

    def test_builds_request(self, monkeypatch):
        created = Grid(
            id="fuel-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_fbfm13_lookup,
            "sync_detailed",
            fake_create,
        )

        result = create_fuel_grid_from_fbfm13_lookup(
            self._source(),
            bands=["fuel_load.1hr", Fbfm13LookupBand.FUEL_DEPTH],
            name="Anderson fuel parameters",
        )

        assert result.id == "fuel-grid-id"
        assert captured["body"].source_grid_id == "fbfm13-grid-id"
        assert captured["body"].source_band == "fbfm13"
        assert captured["body"].bands == [
            Fbfm13LookupBand.FUEL_LOAD_1HR,
            Fbfm13LookupBand.FUEL_DEPTH,
        ]
        assert captured["body"].name == "Anderson fuel parameters"

    def test_lookup_returns_new_pending_grid(self, completed_fbfm13_grid):
        fuel_grid = create_fuel_grid_from_fbfm13_lookup(
            completed_fbfm13_grid,
            bands=["fuel_load.1hr", "fuel_depth"],
            name="throwaway_fbfm13_lookup",
        )
        assert fuel_grid.id != completed_fbfm13_grid.id
        assert fuel_grid.domain_id == completed_fbfm13_grid.domain_id
        assert fuel_grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        fuel_grid.delete()

    def test_requires_completed_source(self):
        with pytest.raises(ValueError, match="look up fuel"):
            create_fuel_grid_from_fbfm13_lookup(
                self._source(status=JobStatus.PENDING),
                bands=["fuel_load.1hr"],
            )

    def test_rejects_non_fbfm13_grid(self):
        with pytest.raises(ValueError, match="fbfm13"):
            create_fuel_grid_from_fbfm13_lookup(
                self._source(band="elevation"),
                bands=["fuel_load.1hr"],
            )


class TestFccsLookup:
    @staticmethod
    def _source(status=JobStatus.COMPLETED, band="fccs"):
        return Grid(
            id="fccs-grid-id",
            domain_id="domain-id",
            status=status,
            source=GridSource(),
            bands=[Band(key=band, type_=BandType.CATEGORICAL, index=0)],
        )

    def test_builds_request(self, monkeypatch):
        created = Grid(
            id="fuel-grid-id",
            domain_id="domain-id",
            status=JobStatus.PENDING,
            source=GridSource(),
            bands=[],
        )
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_fccs_lookup,
            "sync_detailed",
            fake_create,
        )

        result = create_fuel_grid_from_fccs_lookup(
            self._source(),
            bands=["fuel_load.duff", FccsLookupBand.DUFF_DEPTH],
            name="FCCS fuel parameters",
            tags=["test"],
        )

        assert result.id == "fuel-grid-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert captured["body"].source_grid_id == "fccs-grid-id"
        assert captured["body"].source_band == "fccs"
        assert captured["body"].bands == [
            FccsLookupBand.FUEL_LOAD_DUFF,
            FccsLookupBand.DUFF_DEPTH,
        ]
        assert captured["body"].name == "FCCS fuel parameters"
        assert captured["body"].tags == ["test"]

    def test_lookup_returns_new_pending_grid(self, completed_fccs_grid):
        fuel_grid = create_fuel_grid_from_fccs_lookup(
            completed_fccs_grid,
            bands=[
                "fuel_load.litter",
                "fuel_load.duff",
                "duff_depth",
                "fuel_load.live_shrub",
            ],
            name="throwaway_fccs_lookup",
        )
        assert fuel_grid.id != completed_fccs_grid.id
        assert fuel_grid.domain_id == completed_fccs_grid.domain_id
        assert fuel_grid.status in (JobStatus.PENDING, JobStatus.RUNNING)
        fuel_grid.delete()

    def test_requires_completed_source(self):
        with pytest.raises(ValueError, match="look up fuel"):
            create_fuel_grid_from_fccs_lookup(
                self._source(status=JobStatus.PENDING),
                bands=["fuel_load.duff"],
            )

    def test_rejects_non_fccs_grid(self):
        with pytest.raises(ValueError, match="fccs"):
            create_fuel_grid_from_fccs_lookup(
                self._source(band="elevation"),
                bands=["fuel_load.duff"],
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
        # No domain: list grids across all the user's domains. The SDK returns
        # one page at a time, so search subsequent pages when the account has
        # more than the default page size of 100 grids.
        for page in range(100):
            grids = list_grids(
                page=page,
                size=100,
                sort_by="created_on",
                sort_order="descending",
            )
            if completed_topography_grid.id in [grid.id for grid in grids]:
                return
            if len(grids) < 100:
                break

        pytest.fail(
            f"Grid {completed_topography_grid.id} was not found in the "
            "cross-domain grid pages."
        )

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


class TestBandSummary:
    """Unit tests for the band-summary accessor (no API), plus a live check."""

    def _grid_with_band(self, band):
        return Grid(
            id="g",
            domain_id="d",
            status=JobStatus.COMPLETED,
            source=GridSource(),
            bands=[band],
        )

    def test_returns_band_summary(self):
        summary = ContinuousBandSummary(
            type_="continuous",
            count=10,
            nodata_count=0,
            min_=1.0,
            max_=5.0,
            mean=3.0,
            std=1.0,
        )
        grid = self._grid_with_band(
            Band(key="elevation", type_=BandType.CONTINUOUS, index=0, summary=summary)
        )
        assert grid.band_summary("elevation") is summary
        assert grid.band_summary("elevation").mean == 3.0

    def test_none_when_not_computed(self):
        # summary defaults to UNSET (e.g. a pending grid) -> normalized to None
        grid = self._grid_with_band(
            Band(key="elevation", type_=BandType.CONTINUOUS, index=0)
        )
        assert grid.band_summary("elevation") is None

    def test_unknown_band_raises(self):
        grid = self._grid_with_band(
            Band(key="elevation", type_=BandType.CONTINUOUS, index=0)
        )
        with pytest.raises(ValueError, match="no band"):
            grid.band_summary("nope")

    def test_continuous_summary_live(self, completed_topography_grid):
        summary = completed_topography_grid.band_summary("elevation")
        assert summary.type_ == "continuous"
        assert summary.count > 0
        assert summary.mean is not None
