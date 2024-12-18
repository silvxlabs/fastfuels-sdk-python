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
    SurfaceGridAttribute,
    SurfaceGridModification,
    Export,
    GridAttributeMetadataResponse,
)
from fastfuels_sdk.utils import parse_dict_items_to_pydantic_list

_SURFACE_GRID_API = SurfaceGridApi(get_client())


class SurfaceGridBuilder:
    """Builder for creating surface grids with complex attribute configurations."""

    def __init__(self, domain_id: str):
        self.domain_id = domain_id
        self.attributes: List[str] = []
        self.config = {}

    # Fuel Load Methods
    def with_uniform_fuel_load(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform fuel load value.

        Parameters
        ----------
        value : float
            Fuel load value in kg/m²

        Examples
        --------
        >>> builder.with_uniform_fuel_load(0.5)
        """
        self.attributes.append(SurfaceGridAttribute.FUELLOAD)
        self.config["fuel_load"] = {"source": "uniform", "value": value}
        return self

    def with_fuel_load_from_landfire(
        self, product: str, version: str = "2022", interpolation_method: str = "nearest"
    ) -> "SurfaceGridBuilder":
        """Configure fuel load from LANDFIRE source.

        Parameters
        ----------
        product : str
            LANDFIRE product name ("FBFM40" or "FBFM13")
        version : str, optional
            LANDFIRE version, default "2022"
        interpolation_method : str, optional
            Method for interpolation, default "nearest"

        Examples
        --------
        >>> builder.with_fuel_load_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest"
        ... )
        """
        self.attributes.append(SurfaceGridAttribute.FUELLOAD)
        # TODO: Instantiate the Pydantic model directly
        self.config["fuel_load"] = {
            "source": "LANDFIRE",
            "product": product,
            "version": version,
            "interpolation_method": interpolation_method,
        }
        return self

    # Fuel Moisture Methods (only supports uniform)
    def with_uniform_fuel_moisture(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform fuel moisture value.

        Parameters
        ----------
        value : float
            Fuel moisture value as percentage (0-100)

        Examples
        --------
        >>> builder.with_uniform_fuel_moisture(15.0)  # 15%
        """
        self.attributes.append("fuelMoisture")
        self.config["fuelMoisture"] = {"source": "uniform", "value": value}
        return self

    def with_uniform_fbfm(self, value: int) -> "SurfaceGridBuilder":
        """Set uniform Fire Behavior Fuel Model.

        Parameters
        ----------
        value : int
            FBFM value (typically 1-13 for A13, 1-40 for SB40)

        Examples
        --------
        >>> builder.with_uniform_fbfm(9)  # Anderson Model 9
        """
        self.attributes.append("FBFM")
        self.config["FBFM"] = {"source": "uniform", "value": value}
        return self

    def with_fbfm_from_landfire(
        self,
        product: str = "FBFM40",  # Literal["FBFM40", "FBFM13"],
        version: str = "2022",
        interpolation_method: str = "nearest",
    ) -> "SurfaceGridBuilder":
        """Configure FBFM from LANDFIRE source.

        Parameters
        ----------
        product : str
            LANDFIRE product to use:
            - "FBFM40": Scott & Burgan 40 fuel models
            - "FBFM13": Anderson 13 fuel models
        version : str, optional
            LANDFIRE version, default "2022"
        interpolation_method : str, optional
            Method for interpolation, default "nearest"

        Examples
        --------
        >>> builder.with_fbfm_from_landfire(
        ...     product="FBFM40",  # Scott & Burgan 40 fuel models
        ...     version="2022"
        ... )
        """
        self.attributes.append("FBFM")
        self.config["FBFM"] = {
            "source": "LANDFIRE",
            "product": product,
            "version": version,
            "interpolationMethod": interpolation_method,
        }
        return self

    def with_uniform_savr(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform Surface Area to Volume Ratio.

        Parameters
        ----------
        value : float
            Surface Area to Volume Ratio in 1/m

        Examples
        --------
        >>> builder.with_uniform_savr(2000)  # 2000/m
        """
        self.attributes.append("SAVR")
        self.config["SAVR"] = {"source": "uniform", "value": value}
        return self

    def with_savr_from_landfire(
        self, product: str, version: str = "2022", interpolation_method: str = "nearest"
    ) -> "SurfaceGridBuilder":
        """Configure SAVR from LANDFIRE source."""
        self.attributes.append("SAVR")
        self.config["SAVR"] = {
            "source": "LANDFIRE",
            "product": product,
            "version": version,
            "interpolationMethod": interpolation_method,
        }
        return self

    def with_uniform_fuel_depth(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform fuel depth value.

        Parameters
        ----------
        value : float
            Fuel depth in meters

        Examples
        --------
        >>> builder.with_uniform_fuel_depth(0.3)  # 30cm depth
        """
        self.attributes.append("fuelDepth")
        self.config["fuelDepth"] = {"source": "uniform", "value": value}
        return self

    def with_fuel_depth_from_landfire(
        self, product: str, version: str = "2022", interpolation_method: str = "nearest"
    ) -> "SurfaceGridBuilder":
        """Configure fuel depth from LANDFIRE source."""
        self.attributes.append("fuelDepth")
        self.config["fuelDepth"] = {
            "source": "LANDFIRE",
            "product": product,
            "version": version,
            "interpolationMethod": interpolation_method,
        }
        return self

    def with_modification(
        self, conditions: dict, attributes: dict
    ) -> "SurfaceGridBuilder":
        """Add a modification to the surface grid.

        Parameters
        ----------
        conditions : dict
            Conditions for the modification
        attributes : dict
            Attributes to modify

        # TODO: Update examples
        # Examples
        # --------
        # >>> builder.with_modification(
        # ...     conditions={"slope": {"min": 0, "max": 10}},
        # ...     attributes={"fuelLoad": 0.6}
        # ... )
        """
        self.config.setdefault("modifications", []).append(
            {"conditions": conditions, "attributes": attributes}
        )
        return self

    def build(self) -> "SurfaceGrid":
        """Create the surface grid with configured attributes.

        Examples
        --------
        >>> grid = (SurfaceGridBuilder("abc123")
        ...     .with_uniform_fuel_load(0.5)
        ...     .with_uniform_fuel_moisture(15.0)
        ...     .with_fbfm_from_landfire("FBFM40")
        ...     .build())
        """
        return SurfaceGrid.create(
            domain_id=self.domain_id, attributes=self.attributes, **self.config
        )

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "attributes": self.attributes,
            **self.config,
        }


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
        """
        request = CreateSurfaceGridRequest(
            attributes=attributes,  # type: ignore # pydantic handles this
            fuel_load=fuel_load,
            fuel_depth=fuel_depth,
            fuel_moisture=fuel_moisture,
            savr=savr,
            fbfm=fbfm,
            modifications=(
                parse_dict_items_to_pydantic_list(
                    modifications, SurfaceGridModification
                )
            ),
        )

        response = _SURFACE_GRID_API.create_surface_grid(
            domain_id=domain_id, create_surface_grid_request=request
        )
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
