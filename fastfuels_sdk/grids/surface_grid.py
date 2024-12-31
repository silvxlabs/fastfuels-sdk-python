"""
fastfuels_sdk/grids/surface_grid.py
"""

# Core imports
from __future__ import annotations
from typing import List, Optional

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.client_library.api import SurfaceGridApi
from fastfuels_sdk.client_library.models import (
    SurfaceGrid as SurfaceGridModel,
    CreateSurfaceGridRequest,
    SurfaceGridModification,
    SurfaceGridFuelLoad,
    SurfaceGridFuelDepth,
    SurfaceGridFuelMoisture,
    SurfaceGridSAVR,
    SurfaceGridFBFM,
    Export,
    GridAttributeMetadataResponse,
)

_SURFACE_GRID_API = SurfaceGridApi(get_client())


class SurfaceGrid(SurfaceGridModel):
    """Surface grid data within a domain's spatial boundaries."""

    domain_id: str

    @classmethod
    def from_domain(cls, domain_id: str) -> "SurfaceGrid":
        """Retrieve an existing surface grid for a domain.

        Parameters
        ----------
        domain_id : str
            ID of the domain to retrieve surface grid for

        Returns
        -------
        SurfaceGrid
            The surface grid object

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grid = SurfaceGrid.from_domain(domain)
        >>> print(grid.status)
        'completed'
        """
        response = _SURFACE_GRID_API.get_surface_grid(domain_id=domain_id)
        return cls(domain_id=domain_id, **response.model_dump())

    @classmethod
    def create(
        cls,
        domain_id: str,
        attributes: List[str],
        fuel_load: Optional[dict] = None,
        fuel_depth: Optional[dict] = None,
        fuel_moisture: Optional[dict] = None,
        savr: Optional[dict] = None,
        fbfm: Optional[dict] = None,
        modifications: Optional[dict | list[dict]] = None,
    ) -> "SurfaceGrid":
        """Create a new surface grid.

        Parameters
        ----------
        domain_id : str
            ID of domain to create grid for
        attributes : List[str]
            List of attributes to include ("fuelLoad", "fuelDepth", etc.)
        fuel_load : dict, optional
            Configuration for fuel load attribute:
            - Uniform: {"source": "uniform", "value": float}
            - LANDFIRE: {
                "source": "LANDFIRE",
                "product": str,
                "version": str,
                "interpolationMethod": str
              }
        fuel_moisture : dict, optional
            Configuration for fuel moisture (uniform only)
        fbfm : dict, optional
            Configuration for Fire Behavior Fuel Model

        Examples
        --------
        # Create with uniform values
        >>> grid = SurfaceGrid.create(
        ...     domain_id="abc123",
        ...     attributes=["fuelLoad", "fuelMoisture"],
        ...     fuel_load={"source": "uniform", "value": 0.5},
        ...     fuel_moisture={"source": "uniform", "value": 0.1}
        ... )

        # Create with LANDFIRE source
        >>> grid = SurfaceGrid.create(
        ...     domain_id="abc123",
        ...     attributes=["fuelLoad", "FBFM"],
        ...     fuel_load={
        ...         "source": "LANDFIRE",
        ...         "product": "FBFM40",
        ...         "version": "2022",
        ...         "interpolationMethod": "nearest"
        ...     }
        ... )

        See Also
        --------
        SurfaceGridBuilder: Helper object for creating surface grid configurations.
        """
        request = CreateSurfaceGridRequest(
            attributes=attributes,  # type: ignore # pydantic handles this
            fuel_load=SurfaceGridFuelLoad.from_dict(fuel_load) if fuel_load else None,
            fuel_depth=(
                SurfaceGridFuelDepth.from_dict(fuel_depth) if fuel_depth else None
            ),
            fuel_moisture=(
                SurfaceGridFuelMoisture.from_dict(fuel_moisture)
                if fuel_moisture
                else None
            ),
            savr=SurfaceGridSAVR.from_dict(savr) if savr else None,
            fbfm=SurfaceGridFBFM.from_dict(fbfm) if fbfm else None,
            modifications=(
                SurfaceGridModification.from_dict(modifications)
                if modifications
                else None
            ),
        )

        response = _SURFACE_GRID_API.create_surface_grid(
            domain_id=domain_id, create_surface_grid_request=request
        )
        return_object = cls(domain_id=domain_id, **response.model_dump())
        return_object.fuel_load = response.fuel_load
        return_object.fuel_depth = response.fuel_depth
        return_object.fuel_moisture = response.fuel_moisture
        return_object.savr = response.savr
        return_object.fbfm = response.fbfm

        return return_object

    def get(self, in_place: bool = False) -> "SurfaceGrid":
        """Get the latest surface grid data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this SurfaceGrid instance with new data.
            If False (default), returns a new SurfaceGrid instance.

        Returns
        -------
        SurfaceGrid
            The updated surface grid object

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grid = SurfaceGrid.from_domain(domain)

        >>> # Get fresh data in a new instance
        >>> updated_grid = grid.get()

        >>> # Or update the existing instance
        >>> grid.get(in_place=True)
        """
        response = _SURFACE_GRID_API.get_surface_grid(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return SurfaceGrid(domain_id=self.domain_id, **response.model_dump())

    def get_attributes(self) -> GridAttributeMetadataResponse:
        """Get metadata about grid attributes.

        Returns metadata about the structure of the surface grid and its attributes,
        including dimensions, chunking, and attribute details.

        Returns
        -------
        GridAttributeMetadataResponse
            Metadata about grid structure and attributes including:
            - shape: Dimensions of the grid data
            - dimensions: Names of each dimension
            - chunks: Number of chunks in each dimension
            - chunk_shape: Shape of each chunk
            - attributes: Detailed information about each attribute

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grid = SurfaceGrid.from_domain(domain)
        >>> metadata = grid.get_attributes()
        >>> print(metadata.shape)
        [100, 100, 50]
        """
        return _SURFACE_GRID_API.get_surface_grid_attribute_metadata(
            domain_id=self.domain_id
        )

    def create_export(self, export_format: str) -> Export:
        """Create an export of the surface grid data.

        Parameters
        ----------
        export_format : str
            Format for the export. Must be one of:
            - "zarr": Compressed array format
            - "geotiff": GeoTIFF format

        Returns
        -------
        Export
            Export object for managing the export process

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grid = SurfaceGrid.from_domain(domain)
        >>> export = grid.create_export("zarr")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zarr")
        """
        response = _SURFACE_GRID_API.create_surface_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def get_export(self, export_format: str) -> Export:
        """Get the status of an existing export.

        Parameters
        ----------
        export_format : str
            Format of the export to check. Must be one of:
            - "zarr": Compressed array format
            - "geotiff": GeoTIFF format

        Returns
        -------
        Export
            Export object containing current status

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grid = SurfaceGrid.from_domain(domain)
        >>> export = grid.create_export("zarr")
        >>> # Check status later
        >>> export = grid.get_export("zarr")
        >>> if export.status == "completed":
        ...     export.to_file("grid_data.zarr")
        """
        response = _SURFACE_GRID_API.get_surface_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def delete(self) -> None:
        """Delete this surface grid.

        Permanently removes surface grid data from the domain. This also cancels
        any ongoing processing jobs.

        Returns
        -------
        None

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grid = SurfaceGrid.from_domain(domain)
        >>> # Remove grid when no longer needed
        >>> grid.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> grid.get()  # raises NotFoundException
        """
        _SURFACE_GRID_API.delete_surface_grid(domain_id=self.domain_id)
        return None
