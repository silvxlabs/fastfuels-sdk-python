"""
fastfuels_sdk/grids/tree_grid.py
"""

# Core imports
from __future__ import annotations
from typing import List

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.client_library.api import TreeGridApi
from fastfuels_sdk.client_library.models import (
    TreeGrid as TreeGridModel,
    GridAttributeMetadataResponse,
    Export,
)

_TREE_GRID_API = TreeGridApi(get_client())


class TreeGrid(TreeGridModel):
    """3D gridded tree data within a domain's spatial boundaries.

    Represents tree grid data extracted from various sources and organized into a
    three-dimensional grid structure. Tree grids include information about attributes
    like bulk density, fuel moisture, and species codes at each grid point.

    Attributes
    ----------
    domain_id : str
        ID of the domain this grid belongs to
    attributes : List[TreeGridAttribute], optional
        Grid attributes (bulk_density, fuel_moisture, SPCD)
    status : str, optional
        Current processing status ("pending", "running", "completed")
    created_on : datetime, optional
        When this grid was created
    modified_on : datetime, optional
        When this grid was last modified
    checksum : str, optional
        Unique identifier for this version of the grid
    tree_inventory_checksum : str, optional
        Checksum of tree inventory used to generate grid

    Examples
    --------
    Get existing tree grid:
    >>> domain = Domain.from_id("abc123")
    >>> grids = Grids.from_domain(domain)
    >>> if grids.tree:
    ...     tree_grid = grids.tree

    Create new tree grid:
    >>> attributes = ["bulkDensity", "fuelMoisture"]
    >>> tree_grid = grids.create_tree_grid(attributes=attributes)
    >>> print(tree_grid.status)
    'pending'
    """

    domain_id: str

    @classmethod
    def from_domain_id(cls, domain_id: str) -> TreeGrid:
        """Retrieve an existing tree grid for a domain.

        Parameters
        ----------
        domain : Domain
            The domain whose tree grid should be retrieved

        Returns
        -------
        TreeGrid
            The tree grid object

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> tree_grid = TreeGrid.from_domain(domain)
        >>> tree_grid.status
        'completed'
        """
        response = _TREE_GRID_API.get_tree_grid(domain_id=domain_id)
        return cls(domain_id=domain_id, **response.model_dump())

    def get(self, in_place: bool = False) -> TreeGrid:
        """Get the latest tree grid data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this TreeGrid instance with new data.
            If False (default), returns a new TreeGrid instance.

        Returns
        -------
        TreeGrid
            The updated tree grid object

        Examples
        --------
        >>> from fastfuels_sdk import Domain, TreeGrid
        >>> domain = Domain.from_id("abc123")
        >>> tree_grid = TreeGrid.from_domain(domain)
        >>>
        >>> # Get fresh data in a new instance
        >>> updated_grid = tree_grid.get()
        >>>
        >>> # Or update the existing instance
        >>> tree_grid.get(in_place=True)
        """
        response = _TREE_GRID_API.get_tree_grid(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return TreeGrid(domain_id=self.domain_id, **response.model_dump())

    def get_attributes(self) -> GridAttributeMetadataResponse:
        """Get metadata about grid attributes.

        Returns metadata about the structure of the tree grid and its attributes,
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
        >>> tree_grid = TreeGrid.from_domain(domain)
        >>> metadata = tree_grid.get_attributes()
        >>> print(metadata.shape)
        [100, 100, 50]
        """
        return _TREE_GRID_API.get_tree_grid_attribute_metadata(domain_id=self.domain_id)

    def create_export(self, export_format: str) -> Export:
        """Create an export of the tree grid data.

        Parameters
        ----------
        export_format : str
            Format for the export. Must be one of:
            - "zarr": Compressed array format

        Returns
        -------
        Export
            Export object for managing the export process


        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> tree_grid = TreeGrid.from_domain(domain)
        >>> export = tree_grid.create_export("zarr")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zarr")
        """
        response = _TREE_GRID_API.create_tree_grid_export(
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
            - "QUIC-Fire": Input files for QUIC-Fire model

        Returns
        -------
        Export
            Export object containing current status

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> tree_grid = TreeGrid.from_domain(domain)
        >>> export = tree_grid.create_export("zarr")
        >>> # Check status later
        >>> export = tree_grid.get_export("zarr")
        >>> if export.status == "completed":
        ...     export.to_file("grid_data.zarr")
        """
        response = _TREE_GRID_API.get_tree_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def delete(self) -> None:
        """Delete this tree grid.

        Permanently removes tree grid data from the domain. This also cancels
        any ongoing processing jobs.

        Returns
        -------
        None

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> tree_grid = TreeGrid.from_domain(domain)
        >>> # Remove grid when no longer needed
        >>> tree_grid.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> tree_grid.get()  # raises NotFoundException
        """
        _TREE_GRID_API.delete_tree_grid(domain_id=self.domain_id)
        return None
