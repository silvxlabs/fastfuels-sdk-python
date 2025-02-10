"""
fastfuels_sdk/grids/surface_grid_builder.py
"""

# Core imports
from __future__ import annotations
from typing import List

# Internal imports
from fastfuels_sdk.grids.grids import Grids
from fastfuels_sdk.grids.surface_grid import SurfaceGrid
from fastfuels_sdk.client_library.models import (
    SurfaceGridAttribute,
    SurfaceGridModification,
    SurfaceGridFuelLoadSource,
    SurfaceGridFuelDepthSource,
    SurfaceGridFuelMoistureSource,
    SurfaceGridSAVRSource,
    SurfaceGridFBFMSource,
    SurfaceGridLandfireFBFM40Source,
    SurfaceGridLandfireFBFM40SAVRSource,
    SurfaceGridLandfireFBFM40FuelLoadSource,
    SurfaceGridUniformValueBySizeClass,
    SurfaceGridModificationCondition,
    SurfaceGridModificationAction,
)


class SurfaceGridBuilder:
    """Builder for creating surface grids with complex attribute configurations."""

    def __init__(self, domain_id: str):
        self.domain_id = domain_id
        self.attributes: List[str] = []
        self.config = {}

    def with_uniform_fuel_load(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform fuel load value.

        Parameters
        ----------
        value : float
            Fuel load value in kg/m²

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_load(0.5)
        """
        self.config["fuel_load"] = SurfaceGridFuelLoadSource.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELLOAD)

        return self

    def with_uniform_fuel_load_by_size_class(
        self,
        one_hour: float = None,
        ten_hour: float = None,
        hundred_hour: float = None,
        live_herbaceous: float = None,
        live_woody: float = None,
        groups: List[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel load values by size class.

        Parameters
        ----------
        one_hour : float
            1-hour fuel load value in kg/m².
        ten_hour : float
            10-hour fuel load value in kg/m².
        hundred_hour : float
            100-hour fuel load value in kg/m².
        live_herbaceous : float
            Live herbaceous fuel load value in kg/m².
        live_woody : float
            Live woody fuel load value in kg/m².
        groups : list[str], optional
            List of fuel load groups to include. Can be: "oneHour", "tenHour", "hundredHour", "liveHerbaceous", "liveWoody"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_load_by_size_class(
        ...     one_hour=0.5,
        ...     ten_hour=1.0,
        ...     hundred_hour=2.0,
        ...     groups=["oneHour", "tenHour", "hundredHour"]
        ...

        Notes
        -----
        If a size class is not provided, it will be excluded from the configuration.

        If a size class is included in `groups`, but a value is not provided, then the API will raise an error.

        """
        self.config["fuel_load"] = SurfaceGridUniformValueBySizeClass.from_dict(
            {
                "source": "uniformBySizeClass",
                "oneHour": one_hour,
                "tenHour": ten_hour,
                "hundredHour": hundred_hour,
                "liveHerbaceous": live_herbaceous,
                "liveWoody": live_woody,
                "groups": groups,
            }
        ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELLOAD)

        return self

    def with_fuel_load_from_landfire(
        self,
        product: str,
        version: str = "2022",
        interpolation_method: str = "nearest",
        curing_live_herbaceous: float = 0.0,
        curing_live_woody: float = 0.0,
        groups: List[str] = None,
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
        curing_live_herbaceous : float, optional
            Proportion of live herbaceous fuel that is cured, defaults to 0.
        curing_live_woody : float, optional
            Proportion of live woody fuel that is cured, defaults to 0.
        groups : list[str], optional
            List of fuel load groups to include. Can be: "oneHour", "tenHour", "hundredHour", "liveHerbaceous", "liveWoody"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_fuel_load_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest"
        ... )
        """
        self.config["fuel_load"] = SurfaceGridLandfireFBFM40FuelLoadSource.from_dict(
            {
                "source": "LANDFIRE",
                "product": product,
                "version": version,
                "interpolationMethod": interpolation_method,
                "curingLiveHerbaceous": curing_live_herbaceous,
                "curingLiveWoody": curing_live_woody,
                "groups": groups,
            }
        ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELLOAD)

        return self

    def with_uniform_fuel_depth(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform fuel depth value.

        Parameters
        ----------
        value : float
            Fuel depth in meters

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_depth(0.3)
        """
        self.config["fuel_depth"] = SurfaceGridFuelDepthSource.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELDEPTH)

        return self

    def with_fuel_depth_from_landfire(
        self,
        product: str,
        version: str = "2022",
        interpolation_method: str = "nearest",
    ) -> "SurfaceGridBuilder":
        """Configure fuel depth from LANDFIRE source.

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
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_fuel_depth_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest"
        ... )
        """
        self.config["fuel_depth"] = SurfaceGridLandfireFBFM40Source.from_dict(
            {
                "source": "LANDFIRE",
                "product": product,
                "version": version,
                "interpolationMethod": interpolation_method,
            }
        ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELDEPTH)

        return self

    # Fuel Moisture Methods (only supports uniform)
    def with_uniform_fuel_moisture(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform fuel moisture value.

        Parameters
        ----------
        value : float
            Fuel moisture value (%).

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_moisture(15.0)  # 15%
        """
        self.config["fuel_moisture"] = SurfaceGridFuelMoistureSource.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append("fuelMoisture")

        return self

    def with_uniform_fuel_moisture_by_size_class(
        self,
        one_hour: float,
        ten_hour: float,
        hundred_hour: float,
        live_herbaceous: float,
        live_woody: float,
        groups: List[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel moisture values by size class.

        Parameters
        ----------
        one_hour : float
            1-hour fuel moisture content (%).
        ten_hour : float
            10-hour fuel moisture content (%).
        hundred_hour : float
            100-hour fuel moisture content (%).
        live_herbaceous : float
            Live herbaceous fuel moisture content (%).
        live_woody : float
            Live woody fuel moisture content (%).
        groups : list[str], optional

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_moisture_by_size_class(
        ...     one_hour=10.0,
        ...     ten_hour=15.0,
        ...     hundred_hour=20.0,
        ...     live_herbaceous=75.0,
        ...     live_woody=90.0,
        ...     groups=["oneHour", "tenHour", "hundredHour", "liveHerbaceous", "liveWoody"]
        ... )
        """
        self.config["fuel_moisture"] = SurfaceGridUniformValueBySizeClass.from_dict(
            {
                "source": "uniformBySizeClass",
                "oneHour": one_hour,
                "tenHour": ten_hour,
                "hundredHour": hundred_hour,
                "liveHerbaceous": live_herbaceous,
                "liveWoody": live_woody,
                "groups": groups,
            }
        ).to_dict()
        self.attributes.append("fuelMoisture")

        return self

    def with_uniform_fbfm(self, value: str) -> "SurfaceGridBuilder":
        """Set uniform Fire Behavior Fuel Model.

        Parameters
        ----------
        value : str
            FBFM value (e.g. "9", "GR2")

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fbfm("GR2")
        """
        self.config["fbfm"] = SurfaceGridFBFMSource.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append("FBFM")

        return self

    def with_fbfm_from_landfire(
        self,
        product: str,
        version: str = "2022",
        interpolation_method: str = "nearest",
    ) -> "SurfaceGridBuilder":
        """Configure FBFM from LANDFIRE source.

        Parameters
        ----------
        product : str
            LANDFIRE product to use ("FBFM40" or "FBFM13")
        version : str, optional
            LANDFIRE version, default "2022"
        interpolation_method : str, optional
            Method for interpolation, default "nearest"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_fbfm_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest"
        ... )
        """
        self.config["fbfm"] = SurfaceGridFBFMSource.from_dict(
            {
                "source": "LANDFIRE",
                "product": product,
                "version": version,
                "interpolationMethod": interpolation_method,
            }
        ).to_dict()
        self.attributes.append("FBFM")

        return self

    def with_uniform_savr(self, value: float) -> "SurfaceGridBuilder":
        """Set uniform Surface Area to Volume Ratio (SAVR).

        Parameters
        ----------
        value : float
            SAVR value in m²/m³

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_savr(200.0)
        """
        self.config["savr"] = SurfaceGridSAVRSource.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append("SAVR")

        return self

    # def with_uniform_savr_by_size_class(
    #     self,
    #     one_hour: float,
    #     ten_hour: float,
    #     hundred_hour: float,
    #     live_herbaceous: float,
    #     live_woody: float,
    # ) -> "SurfaceGridBuilder":
    #     """Set uniform SAVR values by size class.
    #
    #     Parameters
    #     ----------
    #     one_hour : float
    #         1-hour SAVR value in m²/m³.
    #     ten_hour : float
    #         10-hour SAVR value in m²/m³.
    #     hundred_hour : float
    #         100-hour SAVR value in m²/m³.
    #     live_herbaceous : float
    #         Live herbaceous SAVR value in m²/m³.
    #     live_woody : float
    #         Live woody SAVR value in m²/m³.
    #     """
    #     self.config["savr"] = SurfaceGridUniformValueBySizeClass.from_dict(
    #         {
    #             "source": "uniformBySizeClass",
    #             "oneHour": one_hour,
    #             "tenHour": ten_hour,
    #             "hundredHour": hundred_hour,
    #             "liveHerbaceous": live_herbaceous,
    #             "liveWoody": live_woody,
    #         }
    #     ).to_dict()
    #     self.attributes.append("SAVR")
    #
    #     return self

    def with_savr_from_landfire(
        self,
        product: str,
        version: str = "2022",
        interpolation_method: str = "nearest",
        groups: List[str] = None,
    ) -> "SurfaceGridBuilder":
        """Configure SAVR from LANDFIRE source.

        Parameters
        ----------
        product : str
            LANDFIRE product to use ("FBFM40" or "FBFM13")
        version : str, optional
            LANDFIRE version, default "2022"
        interpolation_method : str, optional
            Method for interpolation, default "nearest"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_savr_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest"
        ... )
        """
        self.config["savr"] = SurfaceGridLandfireFBFM40SAVRSource.from_dict(
            {
                "source": "LANDFIRE",
                "product": product,
                "version": version,
                "interpolationMethod": interpolation_method,
                "groups": groups,
            }
        ).to_dict()
        self.attributes.append("SAVR")

        return self

    def with_modification(
        self,
        actions: (
            dict
            | list[dict]
            | SurfaceGridModificationAction
            | list[SurfaceGridModificationAction]
        ),
        conditions: (
            dict
            | list[dict]
            | SurfaceGridModificationCondition
            | list[SurfaceGridModificationCondition]
        ) = None,
    ) -> "SurfaceGridBuilder":
        """Add a modification to the surface grid.

        Parameters
        ----------
        actions : dict or list[dict] or SurfaceGridModificationAction or list[SurfaceGridModificationAction]
            Action to apply to the surface grid. Can be a single action or a list of actions.
        conditions : dict or list[dict] or SurfaceGridModificationCondition or list[SurfaceGridModificationCondition], optional
            Condition(s) to apply the action. Can be a single condition or a list of conditions.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_modification(
        ...     actions={"attribute": "FBFM", "modifier": "replace", "value": "GR2"},
        ...     conditions={"attribute": "FBFM", "operator": "eq", "value": "GR1"}
        ... )  # Replace all FBFM values that are GR1 with GR2
        """
        if not isinstance(actions, list):
            actions = [actions]
        if not conditions:
            conditions = []
        if not isinstance(conditions, list):
            conditions = [conditions]

        self.config.setdefault("modifications", []).append(
            SurfaceGridModification.from_dict(
                {"actions": actions, "conditions": conditions}
            ).to_dict()
        )
        return self

    def build(self) -> "SurfaceGrid":
        """Create the surface grid with configured attributes.

        Examples
        --------
        >>> surface_grid = (SurfaceGridBuilder("abc123")
        ...     .with_uniform_fuel_load(0.5)
        ...     .with_uniform_fuel_moisture(15.0)
        ...     .with_fbfm_from_landfire("FBFM40")
        ...     .build())
        """
        grid = Grids.from_domain_id(self.domain_id)
        return grid.create_surface_grid(
            attributes=list(set(self.attributes)),  # Remove duplicates
            **self.config,
        )

    def clear(self) -> "SurfaceGridBuilder":
        """Clear all configured attributes."""
        self.attributes = []
        self.config = {}
        return self

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "attributes": self.attributes,
            **self.config,
        }
