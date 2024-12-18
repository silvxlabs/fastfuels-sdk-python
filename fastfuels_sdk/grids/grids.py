"""
grids.py

This module provides the Grids class for managing grid data associated with a domain
in the FastFuels API.
"""

# Core imports
from __future__ import annotations
from typing import Optional

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.domains import Domain
from fastfuels_sdk.exports import Export
from fastfuels_sdk.client_library.api import (
    GridsApi,
    TreeGridApi,
    SurfaceGridApi,
    TopographyGridApi,
    FeatureGridApi,
)
from fastfuels_sdk.client_library.models import (
    Grids as GridsModel,
    TreeGrid as TreeGridModel,
    SurfaceGrid as SurfaceGridModel,
    TopographyGrid as TopographyGridModel,
    FeatureGrid as FeatureGridModel,
    GridAttributeMetadataResponse,
)

_GRIDS_API = GridsApi(get_client())
_TREE_GRID_API = TreeGridApi(get_client())
_SURFACE_GRID_API = SurfaceGridApi(get_client())
_TOPOGRAPHY_GRID_API = TopographyGridApi(get_client())
_FEATURE_GRID_API = FeatureGridApi(get_client())


class Grids(GridsModel):
    """Container for different types of gridded data within a domain's spatial boundaries.

    A Grids object provides access to various types of gridded data (tree, surface,
    topography, and feature) associated with a specific domain. Each grid type
    represents different aspects of the landscape and can be exported in different
    formats for use in fire behavior modeling.

    Attributes
    ----------
    domain_id : str
        ID of the domain these grids belong to
    tree : TreeGrid, optional
        3D tree canopy data
    surface : SurfaceGrid, optional
        Surface fuel data
    topography : TopographyGrid, optional
        Elevation and terrain data
    feature : FeatureGrid, optional
        Road, water, and other geographic features

    Examples
    --------
    >>> domain = Domain.from_id("abc123")
    >>> grids = Grids.from_domain(domain)

    >>> # Access specific grid types
    >>> if grids.tree:
    ...     print("Domain has tree grid data")
    >>> if grids.surface:
    ...     print("Domain has surface fuel data")

    >>> # Export grids to QUIC-Fire format
    >>> export = grids.create_export("QUIC-Fire")
    >>> export.wait_until_completed()
    >>> export.to_file("grid_data.zip")

    See Also
    --------
    Domain : Spatial container for grids
    TreeGrid : 3D canopy structure
    SurfaceGrid : Surface fuel properties
    TopographyGrid : Elevation data
    FeatureGrid : Geographic features
    """

    domain_id: str
    # tree: Optional[TreeGrid]
    # surface: Optional[SurfaceGrid]
    # topography: Optional[TopographyGrid]
    # feature: Optional[FeatureGrid]

    @classmethod
    def from_domain(cls, domain: Domain) -> Grids:
        """Retrieve the grids associated with a domain.

        Parameters
        ----------
        domain : Domain
            The domain whose grids should be retrieved

        Returns
        -------
        Grids
            A Grids object containing available grid data:
            - tree : TreeGrid, optional
                3D tree canopy data
            - surface : SurfaceGrid, optional
                Surface fuel data
            - topography : TopographyGrid, optional
                Elevation and terrain data
            - feature : FeatureGrid, optional
                Road, water, and other geographic features

        Examples
        --------
        >>> from fastfuels_sdk.domains import Domain
        >>> domain = Domain.from_id("abc123")
        >>> grids = Grids.from_domain(domain)

        >>> # Check for specific grid types
        >>> if grids.tree:
        ...     print("Domain has tree grid data")
        >>> if grids.surface:
        ...     print("Domain has surface grid data")
        """
        grids_response = _GRIDS_API.get_grids(domain_id=domain.id)
        return cls(domain_id=domain.id, **grids_response.model_dump())

    def get(self, in_place: bool = False) -> Grids:
        """Get the latest grid data for this domain.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this Grids instance with new data.
            If False (default), returns a new Grids instance.

        Returns
        -------
        Grids
            The updated Grids object

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grids = Grids.from_domain(domain)

        >>> # Get fresh data in a new instance
        >>> updated_grids = grids.get()

        >>> # Or update the existing instance
        >>> grids.get(in_place=True)
        """
        response = _GRIDS_API.get_grids(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return Grids(domain_id=self.domain_id, **response.model_dump())

    def create_export(self, export_format: str) -> Export:
        """Create an export of the grid data.

        Parameters
        ----------
        export_format : str
            Format to export the data in. Must be one of:
            - "zarr": Compressed array format
            - "QUIC-Fire": Input files for QUIC-Fire model

        Returns
        -------
        Export
            Export object for managing the export process.

        Notes
        -----
        The QUIC-Fire format creates a zip file with:
            - treesrhof.dat: Bulk density data
            - treesmoist.dat: Moisture content data
            - treesdepth.dat: Canopy depth data
            - topo.dat: Topography data (if available)

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grids = Grids.from_domain(domain)
        >>> export = grids.create_export("QUIC-Fire")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zip")
        """
        response = _GRIDS_API.create_grid_export(
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
            Export object containing current status.

        Examples
        --------
        >>> domain = Domain.from_id("abc123")
        >>> grids = Grids.from_domain(domain)
        >>> export = grids.create_export("zarr")
        >>> # Check status later
        >>> export = grids.get_export("zarr")
        >>> if export.status == "completed":
        ...     export.to_file("grid_data.zarr")
        """
        response = _GRIDS_API.get_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())
