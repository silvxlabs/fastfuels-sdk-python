"""
fastfuels_sdk/grids/surface_grid.py
"""

# Core imports
from __future__ import annotations

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.client_library.api import SurfaceGridApi
from fastfuels_sdk.client_library.models import (
    SurfaceGrid as SurfaceGridModel,
    Export,
    GridAttributeMetadataResponse,
)

_SURFACE_GRID_API = SurfaceGridApi(get_client())


class SurfaceGrid(SurfaceGridModel):
    """Surface grid data within a domain's spatial boundaries."""

    domain_id: str

    @classmethod
    def from_domain_id(cls, domain_id: str) -> "SurfaceGrid":
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
        >>> grid = SurfaceGrid.from_domain_id("abc123")
        >>> print(grid.status)
        'completed'
        """
        response = _SURFACE_GRID_API.get_surface_grid(domain_id=domain_id)
        return cls(domain_id=domain_id, **response.model_dump())

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
        >>> from fastfuels_sdk import SurfaceGrid
        >>> grid = SurfaceGrid.from_domain_id("abc123")

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
        >>> from fastfuels_sdk import SurfaceGrid
        >>> grid = SurfaceGrid.from_domain_id("abc123")
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
            An Export object for managing the export process

        Examples
        --------
        >>> from fastfuels_sdk import SurfaceGrid
        >>> grid = SurfaceGrid.from_domain_id("abc123")
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
            An Export object containing current status

        Examples
        --------
        >>> from fastfuels_sdk import SurfaceGrid
        >>> grid = SurfaceGrid.from_domain_id("abc123")
        >>> export = grid.create_export("zarr")
        >>> # Check status later
        >>> updated_export = grid.get_export("zarr")
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
        >>> from fastfuels_sdk import SurfaceGrid
        >>> grid = SurfaceGrid.from_domain_id("abc123")
        >>> # Remove grid when no longer needed
        >>> grid.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> grid.get()  # raises NotFoundException
        """
        _SURFACE_GRID_API.delete_surface_grid(domain_id=self.domain_id)
        return None
