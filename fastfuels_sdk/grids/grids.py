"""
grids.py

This module provides the Grids class for managing grid data associated with a domain
in the FastFuels API.
"""

# Core imports
from __future__ import annotations
from typing import Optional, List

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.exports import Export
from fastfuels_sdk.grids.tree_grid import TreeGrid
from fastfuels_sdk.grids.feature_grid import FeatureGrid
from fastfuels_sdk.grids.surface_grid import SurfaceGrid
from fastfuels_sdk.grids.topography_grid import TopographyGrid
from fastfuels_sdk.client_library.api import (
    GridsApi,
    TreeGridApi,
    SurfaceGridApi,
    TopographyGridApi,
    FeatureGridApi,
)
from fastfuels_sdk.client_library.models import (
    Grids as GridsModel,
    CreateSurfaceGridRequest,
    SurfaceGridFuelLoadSource,
    SurfaceGridFuelDepthSource,
    SurfaceGridFuelMoistureSource,
    SurfaceGridSAVRSource,
    SurfaceGridFBFMSource,
    SurfaceGridModification,
    CreateTopographyGridRequest,
    TopographyGridElevationSource,
    TopographyGridSlopeSource,
    TopographyGridAspectSource,
    CreateTreeGridRequest,
    TreeGridUniformValue,
    TreeGridSPCDSource,
    TreeGridBulkDensitySource,
    CreateFeatureGridRequest,
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
    >>> from fastfuels_sdk import Grids
    >>> grids = Grids.from_domain_id("abc123")

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
    tree: Optional[TreeGrid]
    surface: Optional[SurfaceGrid]
    topography: Optional[TopographyGrid]
    feature: Optional[FeatureGrid]

    @classmethod
    def from_domain_id(cls, domain_id: str) -> Grids:
        """Retrieve the grids associated with a domain.

        Parameters
        ----------
        domain_id : str
            The ID of the domain to retrieve grids for

        Returns
        -------
        Grids
            The grid data for the domain

        Examples
        --------
        >>> grids = Grids.from_domain_id("abc123")

        >>> # Check for specific grid types
        >>> if grids.tree:
        ...     print("Domain has tree grid data")
        >>> if grids.surface:
        ...     print("Domain has surface grid data")
        """
        grids_response = _GRIDS_API.get_grids(domain_id=domain_id)
        response_data = grids_response.model_dump()
        response_data = _convert_api_models_to_sdk_classes(domain_id, response_data)

        return cls(domain_id=domain_id, **response_data)

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
        >>> grids = Grids.from_domain_id("abc123")

        >>> # Get fresh data in a new instance
        >>> updated_grids = grids.get()

        >>> # Or update the existing instance
        >>> grids.get(in_place=True)
        """
        response = _GRIDS_API.get_grids(domain_id=self.domain_id)
        response_data = response.model_dump()
        response_data = _convert_api_models_to_sdk_classes(
            self.domain_id, response_data
        )

        if in_place:
            # Update all attributes of current instance
            for key, value in response_data.items():
                setattr(self, key, value)
            return self

        return Grids(domain_id=self.domain_id, **response_data)

    def create_surface_grid(
        self,
        attributes: List[str],
        fuel_load: Optional[dict] = None,
        fuel_depth: Optional[dict] = None,
        fuel_moisture: Optional[dict] = None,
        savr: Optional[dict] = None,
        fbfm: Optional[dict] = None,
        modifications: Optional[dict | list[dict]] = None,
        in_place: bool = False,
    ) -> SurfaceGrid:
        """Create a surface grid for the current domain.

        Creates a surface grid containing various fuel and vegetation attributes within
        the spatial context of your domain. While this method provides direct creation
        capability, consider using SurfaceGridBuilder for more complex configurations
        and better parameter validation.

        Parameters
        ----------
        attributes : List[str]
            List of attributes to include in the grid. Available attributes:
            - "fuelLoad": Surface fuel loading
            - "fuelDepth": Depth of surface fuels
            - "fuelMoisture": Moisture content of fuels
            - "SAVR": Surface area to volume ratio
            - "FBFM": Fire Behavior Fuel Model

        fuel_load : dict, optional
            Configuration for fuel load attribute. See SurfaceGridBuilder for details.

        fuel_depth : dict, optional
            Configuration for fuel depth attribute. See SurfaceGridBuilder for details.

        fuel_moisture : dict, optional
            Configuration for fuel moisture content. See SurfaceGridBuilder for details.

        savr : dict, optional
            Configuration for surface area to volume ratio. See SurfaceGridBuilder for details.

        fbfm : dict, optional
            Configuration for Fire Behavior Fuel Model. See SurfaceGridBuilder for details.

        modifications : dict or list[dict], optional
            Rules for modifying grid attributes. See SurfaceGridBuilder for details.

        in_place : bool, optional
            If True, updates this object's surface grid (self.surface).
            If False (default), leaves this object unchanged.

        Returns
        -------
        SurfaceGrid
            The newly created surface grid object.

        Notes
        -----
        Grid generation happens asynchronously. The returned grid will initially
        have a "pending" status.

        Examples
        --------
        >>> from fastfuels_sdk import Grids
        >>> grids = Grids.from_domain_id("abc123")

        Simple usage with uniform values:
        >>> grid = grids.create_surface_grid(
        ...     attributes=["fuelLoad", "fuelMoisture"],
        ...     fuel_load={"source": "uniform", "value": 0.5},
        ...     fuel_moisture={"source": "uniform", "value": 0.1}
        ... )

        See Also
        --------
        SurfaceGridBuilder : Helper class for creating complex surface grid configurations
            with parameter validation and a fluent interface.
        """
        request = CreateSurfaceGridRequest(
            attributes=attributes,  # type: ignore # pydantic handles this for us
            fuelLoad=(
                SurfaceGridFuelLoadSource.from_dict(fuel_load) if fuel_load else None
            ),
            fuelDepth=(
                SurfaceGridFuelDepthSource.from_dict(fuel_depth) if fuel_depth else None
            ),
            fuelMoisture=(
                SurfaceGridFuelMoistureSource.from_dict(fuel_moisture)
                if fuel_moisture
                else None
            ),
            SAVR=SurfaceGridSAVRSource.from_dict(savr) if savr else None,
            FBFM=SurfaceGridFBFMSource.from_dict(fbfm) if fbfm else None,
            modifications=(
                SurfaceGridModification.from_dict(modifications)
                if modifications
                else None
            ),
        )

        response = _SURFACE_GRID_API.create_surface_grid(
            domain_id=self.domain_id, create_surface_grid_request=request
        )

        # Create a new SurfaceGrid object with the response data.
        surface_grid = SurfaceGrid(domain_id=self.domain_id, **response.model_dump())

        # For some reason we need to explicitly set the attribute attributes of the object.
        # I'm not sure why we need to do this, but the object doesn't serialize correctly otherwise.
        surface_grid.fuel_load = response.fuel_load
        surface_grid.fuel_depth = response.fuel_depth
        surface_grid.fuel_moisture = response.fuel_moisture
        surface_grid.savr = response.savr
        surface_grid.fbfm = response.fbfm

        if in_place:
            self.surface = surface_grid

        return surface_grid

    def create_topography_grid(
        self,
        attributes: List[str],
        elevation: Optional[dict] = None,
        slope: Optional[dict] = None,
        aspect: Optional[dict] = None,
        in_place: bool = False,
    ) -> TopographyGrid:
        """Create a topography grid for the current domain.

        Creates a topography grid containing elevation, slope, and/or aspect data within
        the spatial context of your domain.

        Parameters
        ----------
        attributes : List[str]
            List of attributes to include in the grid. Available attributes:
            - "elevation": Terrain elevation above sea level
            - "slope": Slope of terrain surface
            - "aspect": Direction the slope faces

        elevation : dict, optional
            Configuration for elevation attribute. Sources available:
            - 3DEP (default):
                {
                    "source": "3DEP",
                    "interpolationMethod": "cubic"  # or "nearest", "linear"
                }
            - LANDFIRE:
                {
                    "source": "LANDFIRE",
                    "version": "2020",
                    "interpolationMethod": "cubic"  # or "nearest", "linear", "zipper"
                }
            - Uniform:
                {
                    "source": "uniform",
                    "value": float  # elevation in meters
                }

        slope : dict, optional
            Configuration for slope attribute. Sources available:
            - 3DEP (default):
                {
                    "source": "3DEP",
                    "interpolationMethod": "cubic"  # or "nearest", "linear"
                }
            - LANDFIRE:
                {
                    "source": "LANDFIRE",
                    "version": "2020",
                    "interpolationMethod": "cubic"  # or "nearest", "linear", "zipper"
                }

        aspect : dict, optional
            Configuration for aspect attribute. Sources available:
            - 3DEP (default):
                {
                    "source": "3DEP",
                    "interpolationMethod": "nearest"
                }
            - LANDFIRE:
                {
                    "source": "LANDFIRE",
                    "version": "2020",
                    "interpolationMethod": "nearest"
                }

        in_place : bool, optional
            If True, updates this object's topography grid (self.topography).
            If False (default), leaves this object unchanged.

        Returns
        -------
        TopographyGrid
            The newly created topography grid object.

        Notes
        -----
        Grid generation happens asynchronously. The returned grid will initially
        have a "pending" status.

        Examples
        --------
        >>> from fastfuels_sdk import Grids
        >>> grids = Grids.from_domain_id("abc123")

        Simple usage with default 3DEP source:
        >>> grid = grids.create_topography_grid(
        ...     attributes=["elevation", "slope"]
        ... )

        Using multiple data sources:
        >>> grid = grids.create_topography_grid(
        ...     attributes=["elevation", "slope", "aspect"],
        ...     elevation={
        ...         "source": "LANDFIRE",
        ...         "version": "2020",
        ...         "interpolationMethod": "cubic"
        ...     },
        ...     slope={
        ...         "source": "3DEP",
        ...         "interpolationMethod": "cubic"
        ...     }
        ... )
        """
        request = CreateTopographyGridRequest(
            attributes=attributes,  # type: ignore # pydantic handles this for us
            elevation=(
                TopographyGridElevationSource.from_dict(elevation)
                if elevation
                else None
            ),
            slope=(TopographyGridSlopeSource.from_dict(slope) if slope else None),
            aspect=(TopographyGridAspectSource.from_dict(aspect) if aspect else None),
        )

        response = _TOPOGRAPHY_GRID_API.create_topography_grid(
            domain_id=self.domain_id, create_topography_grid_request=request
        )

        # Create a new TopographyGrid object with the response data
        topography_grid = TopographyGrid(
            domain_id=self.domain_id, **response.model_dump()
        )

        if in_place:
            self.topography = topography_grid

        return topography_grid

    def create_tree_grid(
        self,
        attributes: List[str],
        bulk_density: Optional[dict] = None,
        spcd: Optional[dict] = None,
        fuel_moisture: Optional[dict] = None,
        in_place: bool = False,
    ) -> TreeGrid:
        """Create a tree grid for the current domain.

        Creates a tree grid containing canopy bulk density, species codes, and/or fuel moisture
        data within the spatial context of your domain. While this method provides direct creation
        capability, consider using TreeGridBuilder for more complex configurations and better
        parameter validation.

        Parameters
        ----------
        attributes : List[str]
            List of attributes to include in the grid. Available attributes:
            - "bulkDensity": Canopy bulk density
            - "SPCD": Species code
            - "fuelMoisture": Moisture content

        bulk_density : dict, optional
            Configuration for bulk density attribute. Sources available:
            - Inventory:
                {
                    "source": "inventory"
                }
            - Uniform:
                {
                    "source": "uniform",
                    "value": float  # bulk density in kg/m³
                }

        spcd : dict, optional
            Configuration for species code attribute. Sources available:
            - Inventory:
                {
                    "source": "inventory"
                }
            - Uniform:
                {
                    "source": "uniform",
                    "value": str  # species code
                }

        fuel_moisture : dict, optional
            Configuration for fuel moisture content. Only supports uniform values:
            {
                "source": "uniform",
                "value": float  # moisture content in %
            }

        in_place : bool, optional
            If True, updates this object's tree grid (self.tree).
            If False (default), leaves this object unchanged.

        Returns
        -------
        TreeGrid
            The newly created tree grid object.

        Notes
        -----
        Grid generation happens asynchronously. The returned grid will initially
        have a "pending" status.

        Examples
        --------
        >>> from fastfuels_sdk import Grids
        >>> grids = Grids.from_domain_id("abc123")

        Simple usage with uniform values:
        >>> grid = grids.create_tree_grid(
        ...     attributes=["bulkDensity", "fuelMoisture"],
        ...     bulk_density={"source": "uniform", "value": 0.5},
        ...     fuel_moisture={"source": "uniform", "value": 15.0}
        ... )

        Using inventory data:
        >>> grid = grids.create_tree_grid(
        ...     attributes=["bulkDensity", "SPCD"],
        ...     bulk_density={"source": "inventory"},
        ...     spcd={"source": "inventory"}
        ... )

        See Also
        --------
        TreeGridBuilder : Helper class for creating complex tree grid configurations
            with parameter validation and a fluent interface.
        """
        request = CreateTreeGridRequest(
            attributes=attributes,  # type: ignore # pydantic handles this for us
            bulkDensity=(
                TreeGridBulkDensitySource.from_dict(bulk_density)
                if bulk_density
                else None
            ),
            SPCD=(TreeGridSPCDSource.from_dict(spcd) if spcd else None),
            fuelMoisture=(
                TreeGridUniformValue.from_dict(fuel_moisture) if fuel_moisture else None
            ),
        )

        response = _TREE_GRID_API.create_tree_grid(
            domain_id=self.domain_id, create_tree_grid_request=request
        )

        # Create a new TreeGrid object with the response data
        tree_grid = TreeGrid(domain_id=self.domain_id, **response.model_dump())

        # For consistency with surface grid, explicitly set the attributes
        tree_grid.bulk_density = response.bulk_density
        tree_grid.spcd = response.spcd
        tree_grid.fuel_moisture = response.fuel_moisture

        if in_place:
            self.tree = tree_grid

        return tree_grid

    def create_feature_grid(
        self,
        attributes: List[str],
        in_place: bool = False,
    ) -> FeatureGrid:
        """Create a feature grid for the current domain.

        Creates a feature grid containing various geographic features within the spatial
        context of your domain. Feature grids represent spatial data related to various
        features such as roads, water bodies, and other geographic elements.

        **Feature resources must have a "completed" status before they can be included as attributes to a feature grid.**

        Parameters
        ----------
        attributes : List[str]
            List of feature types to rasterize in the grid. Available attributes
            depend on the specific geographic features in your domain area.

        in_place : bool, optional
            If True, updates this object's feature grid (self.feature).
            If False (default), leaves this object unchanged.

        Returns
        -------
        FeatureGrid
            The newly created feature grid object.

        Notes
        -----
        Grid generation happens asynchronously. The returned grid will initially
        have a "pending" status.

        Examples
        --------
        >>> from fastfuels_sdk import Grids
        >>> grids = Grids.from_domain_id("abc123")

        Simple usage with specific feature types:
        >>> grid = grids.create_feature_grid(
        ...     attributes=["road", "water"]
        ... )

        Create and wait for completion:
        >>> grid = grids.create_feature_grid(
        ...     attributes=["road", "water"],
        ...     in_place=True
        ... )
        >>> grid.wait_until_completed()
        """
        request = CreateFeatureGridRequest(
            attributes=attributes,  # type: ignore # pydantic handles this for us
        )

        response = _FEATURE_GRID_API.create_feature_grid(
            domain_id=self.domain_id, create_feature_grid_request=request
        )

        # Create a new FeatureGrid object with the response data
        feature_grid = FeatureGrid(domain_id=self.domain_id, **response.model_dump())

        if in_place:
            self.feature = feature_grid

        return feature_grid

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
            An Export object for managing the export process.

        Notes
        -----
        The QUIC-Fire format creates a zip file with:
            - treesrhof.dat: Bulk density data
            - treesmoist.dat: Moisture content data
            - treesdepth.dat: Canopy depth data
            - topo.dat: Topography data (if available)

        Examples
        --------
        >>> grids = Grids.from_domain_id("abc123")

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
            An Export object containing current status.

        Examples
        --------
        >>> from fastfuels_sdk import Grids
        >>> grids = Grids.from_domain_id("abc123")
        >>> export = grids.create_export("zarr")
        >>> # Check status later
        >>> updated_export = grids.get_export("zarr")
        >>> if export.status == "completed":
        ...     export.to_file("grid_data.zarr")
        """
        response = _GRIDS_API.get_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())


def _convert_api_models_to_sdk_classes(domain_id, response_data: dict) -> dict:
    """Convert API models to SDK classes with domain_id."""
    if "surface" in response_data and response_data["surface"]:
        response_data["surface"] = SurfaceGrid(
            domain_id=domain_id, **response_data["surface"]
        )
    if "topography" in response_data and response_data["topography"]:
        response_data["topography"] = TopographyGrid(
            domain_id=domain_id, **response_data["topography"]
        )
    if "tree" in response_data and response_data["tree"]:
        response_data["tree"] = TreeGrid(domain_id=domain_id, **response_data["tree"])
    if "feature" in response_data and response_data["feature"]:
        response_data["feature"] = FeatureGrid(
            domain_id=domain_id, **response_data["feature"]
        )
    return response_data
