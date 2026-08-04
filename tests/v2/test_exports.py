"""
tests/v2/test_exports.py
"""

# Core imports
import json
import zipfile
from http import HTTPStatus
from types import SimpleNamespace
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2.exports import (
    Export,
    _field_source,
    _landscape_field_source,
    create_landscape_export,
    create_quicfire_export,
    get_export,
    list_exports,
)
from fastfuels_sdk.v2.grids import (
    create_canopy_fuel_grid_from_landfire,
    create_fuel_grid_from_fbfm40_lookup,
    create_fuel_model_grid_from_landfire_fbfm40,
    create_topography_grid_from_3dep,
    create_uniform_grid,
)
from fastfuels_sdk.v2.client_library.models import (
    Export as ExportModel,
    ExportSource,
    FieldSource,
    JobStatus,
    LandscapeExportAlignmentDomainTarget,
    LandscapeExportAlignmentGridTarget,
    LandscapeFieldSource,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Response
from fastfuels_sdk.v2.exceptions import (
    NotFoundException,
    UnprocessableEntityException,
)

# External imports
import numpy as np
import pytest
import rasterio

# The test_domain, completed_topography_grid, and completed_tree_inventory
# fixtures are session-scoped and shared across modules (tests/v2/conftest.py).
# They are READ-ONLY: tests that mutate or delete create throwaway exports.


class TestFieldSource:
    """Pure unit tests for the (grid, band) translator (no API)."""

    def test_tuple_with_grid_object(self, completed_topography_grid):
        source = _field_source((completed_topography_grid, "elevation"), "topography")
        assert source.grid_id == completed_topography_grid.id
        assert source.band == "elevation"

    def test_tuple_with_grid_id(self):
        source = _field_source(("abc123", "fuel_depth"), "surface_fuel_depth")
        assert source.grid_id == "abc123"

    def test_field_source_passes_through(self):
        source = FieldSource(grid_id="abc123", band="fuel_depth")
        assert _field_source(source, "surface_fuel_depth") is source

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError, match="surface_moisture"):
            _field_source("not-a-pair", "surface_moisture")


def _landscape_roles():
    return {
        "elevation": ("topography-grid", "elevation"),
        "slope": ("topography-grid", "slope"),
        "aspect": ("topography-grid", "aspect"),
        "fuel_model": ("fuel-model-grid", "fbfm"),
        "canopy_cover": ("canopy-grid", "cc"),
        "canopy_height": ("canopy-grid", "chm"),
        "canopy_base_height": ("canopy-grid", "cbh"),
        "canopy_bulk_density": ("canopy-grid", "cbd"),
    }


def _pending_export_model():
    source = ExportSource()
    source.additional_properties = {"name": "landscape"}
    return ExportModel(
        id="landscape-export-id",
        domain_id="domain-id",
        status=JobStatus.PENDING,
        source=source,
    )


class TestLandscapeFieldSource:
    def test_tuple_with_grid_object(self):
        source = _landscape_field_source(
            (SimpleNamespace(id="grid-id"), "elevation"), "elevation"
        )

        assert source.to_dict() == {"grid_id": "grid-id", "band": "elevation"}

    def test_model_passes_through(self):
        source = LandscapeFieldSource(grid_id="grid-id", band="elevation")
        assert _landscape_field_source(source, "elevation") is source

    def test_invalid_value_names_role(self):
        with pytest.raises(ValueError, match="canopy_height"):
            _landscape_field_source("not-a-pair", "canopy_height")


class TestLandscapeExport:
    @staticmethod
    def _mock_endpoint(monkeypatch, response=None):
        captured = {}
        response = response or Response(
            status_code=HTTPStatus.CREATED,
            content=b"",
            headers={},
            parsed=_pending_export_model(),
        )

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return response

        client = object()
        monkeypatch.setattr("fastfuels_sdk.v2.exports.ensure_client", lambda: client)
        monkeypatch.setattr(
            "fastfuels_sdk.v2.exports.create_landscape_export_endpoint.sync_detailed",
            fake_create,
        )
        return captured, client

    def test_builds_request(self, monkeypatch):
        captured, client = self._mock_endpoint(monkeypatch)

        export = create_landscape_export(
            SimpleNamespace(id="domain-id"),
            fire_behavior_fuel_model="fbfm40",
            name="Landscape",
            tags=["test"],
            **_landscape_roles(),
        )

        assert isinstance(export, Export)
        assert export.id == "landscape-export-id"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert captured["body"].alignment is UNSET
        assert captured["body"].fire_behavior_fuel_model.value == "fbfm40"
        assert captured["body"].elevation.to_dict() == {
            "grid_id": "topography-grid",
            "band": "elevation",
        }
        assert captured["body"].canopy_bulk_density.to_dict() == {
            "grid_id": "canopy-grid",
            "band": "cbd",
        }
        assert captured["body"].name == "Landscape"
        assert captured["body"].tags == ["test"]

    def test_domain_alignment(self, monkeypatch):
        captured, _ = self._mock_endpoint(monkeypatch)

        create_landscape_export(
            "domain-id",
            fire_behavior_fuel_model="fbfm40",
            resolution_m=10,
            **_landscape_roles(),
        )

        assert isinstance(
            captured["body"].alignment, LandscapeExportAlignmentDomainTarget
        )
        assert captured["body"].alignment.resolution == 10

    def test_grid_alignment(self, monkeypatch):
        captured, _ = self._mock_endpoint(monkeypatch)

        create_landscape_export(
            "domain-id",
            fire_behavior_fuel_model="fbfm13",
            align_to=SimpleNamespace(id="master-grid"),
            **_landscape_roles(),
        )

        assert isinstance(
            captured["body"].alignment, LandscapeExportAlignmentGridTarget
        )
        assert captured["body"].alignment.grid_id == "master-grid"

    def test_alignment_arguments_are_exclusive(self):
        with pytest.raises(ValueError, match="not both"):
            create_landscape_export(
                "domain-id",
                fire_behavior_fuel_model="fbfm40",
                resolution_m=30,
                align_to="master-grid",
                **_landscape_roles(),
            )

    def test_alignment_error_is_preserved(self, monkeypatch):
        response = Response(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content=b'{"detail":"fuel_model grid is not aligned with landscape"}',
            headers={},
            parsed=None,
        )
        self._mock_endpoint(monkeypatch, response=response)

        with pytest.raises(UnprocessableEntityException) as exc_info:
            create_landscape_export(
                "domain-id",
                fire_behavior_fuel_model="fbfm40",
                **_landscape_roles(),
            )

        assert exc_info.value.detail == (
            "fuel_model grid is not aligned with landscape"
        )

    @pytest.fixture(scope="class")
    def topography_grid(self, test_domain):
        grid = create_topography_grid_from_3dep(
            test_domain,
            source_resolution_m=10,
            output_resolution_m=30,
            bands=["elevation", "slope", "aspect"],
            name="landscape_topography",
            tags=["test"],
        )
        grid.wait()
        return grid

    @pytest.fixture(scope="class")
    def canopy_grid(self, test_domain):
        grid = create_canopy_fuel_grid_from_landfire(
            test_domain,
            output_resolution_m=30,
            bands=["cc", "chm", "cbh", "cbd"],
            name="landscape_canopy",
            tags=["test"],
        )
        grid.wait()
        return grid

    def test_landscape_roundtrip(
        self,
        test_domain,
        topography_grid,
        completed_fbfm40_grid,
        canopy_grid,
        tmp_path,
    ):
        export = create_landscape_export(
            test_domain,
            fire_behavior_fuel_model="fbfm40",
            elevation=(topography_grid, "elevation"),
            slope=(topography_grid, "slope"),
            aspect=(topography_grid, "aspect"),
            fuel_model=(completed_fbfm40_grid, "fbfm"),
            canopy_cover=(canopy_grid, "cc"),
            canopy_height=(canopy_grid, "chm"),
            canopy_base_height=(canopy_grid, "cbh"),
            canopy_bulk_density=(canopy_grid, "cbd"),
            name="test_landscape",
            tags=["test"],
        )
        try:
            assert isinstance(export, Export)
            assert export.status in (JobStatus.PENDING, JobStatus.RUNNING)
            assert export.source["name"] == "landscape"
            assert len(export.source["georeference"]["shape"]) == 2

            export.wait()
            destination = export.to_file(tmp_path / "landscape.tif")
            with rasterio.open(destination) as dataset:
                assert dataset.count == 8
                assert dataset.dtypes == ("int16",) * 8
                assert dataset.descriptions == (
                    "Elevation",
                    "Slope",
                    "Aspect",
                    "Fuel Model",
                    "Canopy Cover",
                    "Canopy Height",
                    "Canopy Base Height",
                    "Canopy Bulk Density",
                )
        finally:
            export.delete()


class TestGridExportLifecycle:
    @pytest.fixture(scope="class")
    def completed_export(self, completed_topography_grid):
        """A completed GeoTIFF export of the shared topography grid."""
        export = completed_topography_grid.export(format="geotiff", tags=["test"])
        export.wait()
        return export

    def test_export_returns_wrapped_record(self, completed_topography_grid):
        export = completed_topography_grid.export(format="geotiff")
        assert isinstance(export, Export)
        assert export.domain_id == completed_topography_grid.domain_id

    def test_completed_export_carries_signed_url(self, completed_export):
        assert completed_export.status == JobStatus.COMPLETED
        assert completed_export.signed_url
        assert completed_export.expires_on is not None

    def test_to_file_explicit_path(self, completed_export, tmp_path):
        destination = completed_export.to_file(tmp_path / "elevation.tif")
        assert destination == tmp_path / "elevation.tif"
        assert destination.stat().st_size > 0

    def test_to_file_directory_uses_default_filename(self, completed_export, tmp_path):
        destination = completed_export.to_file(tmp_path)
        assert destination.parent == tmp_path
        assert destination.stat().st_size > 0

    def test_geotiff_matches_grid_to_numpy(
        self, completed_export, completed_topography_grid, tmp_path
    ):
        # Ground-truth check for Grid.to_numpy: the array it reconstructs from
        # the binary chunk endpoint must match the same grid rendered to a
        # GeoTIFF by the server and read back with rasterio -- an independent
        # reader that applies the georeference, validating absolute orientation
        # too. Reuses the export fixture, so it adds no export job.
        path = completed_export.to_file(tmp_path / "topography.tif")
        expected = completed_topography_grid.to_numpy("elevation")

        with rasterio.open(path) as src:
            band_number = src.descriptions.index("elevation") + 1
            actual = src.read(band_number).astype(float)
            actual[actual == src.nodata] = np.nan

        valid = np.isfinite(actual) & np.isfinite(expected)
        assert valid.any()
        assert np.allclose(actual[valid], expected[valid], rtol=1e-4, atol=1e-2)

    def test_to_file_requires_completed(self, completed_topography_grid):
        export = completed_topography_grid.export(format="geotiff")
        if export.status == JobStatus.COMPLETED:
            pytest.skip("export completed too quickly to test the guard")
        with pytest.raises(ValueError, match="download"):
            export.to_file("nope.tif")

    def test_from_id_and_get_export(self, completed_export):
        fetched = Export.from_id(completed_export.id)
        assert fetched.id == completed_export.id
        assert get_export(completed_export.id).id == completed_export.id

    def test_not_found(self):
        with pytest.raises(NotFoundException):
            Export.from_id(uuid4().hex)

    def test_refresh_returns_self(self, completed_export):
        assert completed_export.refresh() is completed_export

    def test_update_name(self, completed_export):
        updated = completed_export.update(name="updated_export")
        assert updated is completed_export
        assert get_export(completed_export.id).name == "updated_export"

    def test_update_no_fields_makes_no_api_call(self, completed_export):
        assert completed_export.update() is completed_export

    def test_list_exports(self, test_domain, completed_export):
        export_ids = [e.id for e in list_exports(test_domain)]
        assert completed_export.id in export_ids

    def test_list_exports_tag_filter(self, completed_export):
        export_ids = [e.id for e in list_exports(tag="test")]
        assert completed_export.id in export_ids

    def test_to_json(self, completed_export):
        export_dict = json.loads(completed_export.to_json())
        assert export_dict["id"] == completed_export.id

    def test_delete(self, completed_topography_grid):
        export = completed_topography_grid.export(format="geotiff")
        export.delete()
        with pytest.raises(NotFoundException):
            Export.from_id(export.id)


class TestInventoryExport:
    def test_csv_roundtrip(self, completed_tree_inventory, tmp_path):
        export = completed_tree_inventory.export(format="csv")
        assert isinstance(export, Export)
        export.wait()
        destination = export.to_file(tmp_path / "trees.csv")
        header = destination.read_text().splitlines()[0]
        assert "height" in header


class TestQuicfireExport:
    @pytest.fixture(scope="class")
    def voxel_grid(self, completed_tree_inventory):
        """A 3D canopy grid carrying bulk density + moisture bands."""
        voxels = completed_tree_inventory.voxelize(
            horizontal_resolution_m=2.0,
            vertical_resolution_m=1.0,
            bands=["bulk_density.foliage.live", "fuel_moisture.live"],
            name="qf_voxels",
        )
        voxels.wait()
        return voxels

    @pytest.fixture(scope="class")
    def surface_grid(self, test_domain):
        """A 2 m uniform surface grid carrying load, depth, and moisture."""
        grid = create_uniform_grid(
            test_domain,
            resolution_m=2.0,
            bands={
                "fuel_load.1hr": 0.5,
                "fuel_depth": 0.3,
                "fuel_moisture.1hr": 10.0,
            },
            name="qf_surface",
        )
        grid.wait()
        return grid

    @pytest.fixture(scope="class")
    def lookup_surface_grid(self, test_domain):
        """Surface load + depth from a real FBFM40 lookup, on the 2 m lattice.

        Unlike the uniform ``surface_grid``, this is a genuine data-derived
        grid: an FBFM40 grid built on the 2 m domain lattice, then looked up
        into fuel-parameter bands. It must align cell-for-cell with the fire
        grid (which defaults to the domain bbox at 2 m) for the export to
        slice it without resampling.
        """
        fbfm = create_fuel_model_grid_from_landfire_fbfm40(
            test_domain, output_resolution_m=2.0, name="qf_fbfm"
        )
        fbfm.wait()
        surface = create_fuel_grid_from_fbfm40_lookup(
            fbfm, bands=["fuel_load.1hr", "fuel_depth"], name="qf_surface_lookup"
        )
        surface.wait()
        return surface

    @pytest.fixture(scope="class")
    def aligned_topography_grid(self, test_domain):
        """3DEP elevation on the 2 m lattice, so it aligns with the fire grid."""
        grid = create_topography_grid_from_3dep(
            test_domain,
            source_resolution_m=10,
            output_resolution_m=2.0,
            bands=["elevation"],
            name="qf_topo",
        )
        grid.wait()
        return grid

    def test_align_to_excludes_resolution(self, test_domain, voxel_grid):
        with pytest.raises(ValueError, match="not both"):
            create_quicfire_export(
                test_domain,
                canopy_bulk_density=(voxel_grid, "bulk_density.foliage.live"),
                canopy_moisture=(voxel_grid, "fuel_moisture.live"),
                surface_fuel_load=("g", "fuel_load.1hr"),
                surface_fuel_depth=("g", "fuel_depth"),
                surface_moisture=("g", "fuel_moisture.1hr"),
                align_to=voxel_grid,
                horizontal_resolution_m=2.0,
            )

    def test_bundle_roundtrip(self, test_domain, voxel_grid, surface_grid, tmp_path):
        export = create_quicfire_export(
            test_domain,
            canopy_bulk_density=(voxel_grid, "bulk_density.foliage.live"),
            canopy_moisture=(voxel_grid, "fuel_moisture.live"),
            surface_fuel_load=(surface_grid, "fuel_load.1hr"),
            surface_fuel_depth=(surface_grid, "fuel_depth"),
            surface_moisture=(surface_grid, "fuel_moisture.1hr"),
            name="qf_bundle",
        )
        assert isinstance(export, Export)
        assert export.status in (JobStatus.PENDING, JobStatus.RUNNING)
        export.wait()

        destination = export.to_file(tmp_path)
        with zipfile.ZipFile(destination) as archive:
            names = set(archive.namelist())
        assert {
            "treesrhof.dat",
            "treesmoist.dat",
            "treesfueldepth.dat",
            "metadata.json",
            "domain.geojson",
        } <= names
        export.delete()

    def test_bundle_with_lookup_surface_and_topography(
        self,
        test_domain,
        voxel_grid,
        lookup_surface_grid,
        surface_grid,
        aligned_topography_grid,
        tmp_path,
    ):
        # The realistic QUIC-Fire workflow (and the export tutorial): surface
        # load/depth come from a data-derived FBFM40 lookup grid rather than a
        # uniform grid, and a 3DEP topography grid is supplied -- so the bundle
        # must additionally contain topo.dat. Every role grid sits on the 2 m
        # fire-grid lattice; the exporter crops but never resamples, so this
        # also guards that an FBFM40-lookup grid and a 3DEP grid align with the
        # voxel grid cell-for-cell.
        export = create_quicfire_export(
            test_domain,
            canopy_bulk_density=(voxel_grid, "bulk_density.foliage.live"),
            canopy_moisture=(voxel_grid, "fuel_moisture.live"),
            surface_fuel_load=(lookup_surface_grid, "fuel_load.1hr"),
            surface_fuel_depth=(lookup_surface_grid, "fuel_depth"),
            surface_moisture=(surface_grid, "fuel_moisture.1hr"),
            topography=(aligned_topography_grid, "elevation"),
            name="qf_realistic",
        )
        assert isinstance(export, Export)
        export.wait()

        destination = export.to_file(tmp_path)
        with zipfile.ZipFile(destination) as archive:
            names = set(archive.namelist())
        assert {
            "treesrhof.dat",
            "treesmoist.dat",
            "treesfueldepth.dat",
            "topo.dat",
            "metadata.json",
            "domain.geojson",
        } <= names
        export.delete()
