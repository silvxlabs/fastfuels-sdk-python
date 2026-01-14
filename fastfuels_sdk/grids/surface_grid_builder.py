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
    Fuelload,
    Fueldepth,
    SurfaceGridFuelMoistureSource,
    SurfaceGridSAVRSource,
    SurfaceGridFBFMSource,
    SurfaceGridLandfireFBFM40Source,
    SurfaceGridLandfireFBFM40SAVRSource,
    SurfaceGridLandfireFBFM40FuelLoadSource,
    SurfaceGridUniformValueBySizeClass,
    SurfaceGridModificationCondition,
    SurfaceGridModificationAction,
    SurfaceGridLandfireFCCSFuelLoadSource,
    SurfaceGridLandfireFCCSSource,
)


class SurfaceGridBuilder:
    """Builder for creating surface grids with complex attribute configurations."""

    def __init__(self, domain_id: str):
        self.domain_id = domain_id
        self.attributes: List[str] = []
        self.config = {}

    def with_uniform_fuel_load(
        self, value: float, feature_masks: list[str] = None
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel load value.

        Parameters
        ----------
        value : float
            Fuel load value in kg/m²
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_load(value=0.5, feature_masks=["road", "water"])
        """
        self.config["fuel_load"] = Fuelload.from_dict(
            {"source": "uniform", "value": value, "featureMasks": feature_masks}
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
        feature_masks: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel load values by size class.

        Parameters
        ----------
        one_hour : float, optional
            1-hour fuel load value in kg/m².
        ten_hour : float, optional
            10-hour fuel load value in kg/m².
        hundred_hour : float, optional
            100-hour fuel load value in kg/m².
        live_herbaceous : float, optional
            Live herbaceous fuel load value in kg/m².
        live_woody : float, optional
            Live woody fuel load value in kg/m².
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_load_by_size_class(
        ...     one_hour=0.5,
        ...     ten_hour=1.0,
        ...     hundred_hour=2.0,
        ...     feature_masks=["road", "water"]
        ... )

        Notes
        -----
        Only size classes with provided values will be included in the configuration.
        """
        # Map parameter names to their corresponding group names in camelCase
        param_to_group = {
            "one_hour": "oneHour",
            "ten_hour": "tenHour",
            "hundred_hour": "hundredHour",
            "live_herbaceous": "liveHerbaceous",
            "live_woody": "liveWoody",
        }

        # Build the groups list based on which parameters have values
        groups = []
        for param_name, group_name in param_to_group.items():
            if locals()[param_name] is not None:
                groups.append(group_name)

        # Create the configuration dictionary
        self.config["fuel_load"] = SurfaceGridUniformValueBySizeClass.from_dict(
            {
                "source": "uniformBySizeClass",
                "oneHour": one_hour,
                "tenHour": ten_hour,
                "hundredHour": hundred_hour,
                "liveHerbaceous": live_herbaceous,
                "liveWoody": live_woody,
                "groups": groups,
                "featureMasks": feature_masks,
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
        feature_masks: list[str] = None,
        remove_non_burnable: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Configure fuel load from LANDFIRE source.

        Parameters
        ----------
        product : str
            LANDFIRE product name ("FBFM40", "FBFM13", or "FCCS")
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
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.
        remove_non_burnable : list[str], optional
            List of non-burnable fuel models to remove. This option is often used in conjunction with feature_masks to improve the resolution of landscape features. Can be: "NB1", "NB2", "NB3", "NB8", "NB9"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_fuel_load_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest",
        ...     curing_live_herbaceous=0.25,
        ...     curing_live_woody=0.1,
        ...     groups=["oneHour", "tenHour", "hundredHour"],
        ...     feature_masks=["road", "water"],
        ...     remove_non_burnable=["NB1", "NB2"]
        ... )
        """
        if product == "FBFM40":
            self.config["fuel_load"] = (
                SurfaceGridLandfireFBFM40FuelLoadSource.from_dict(
                    {
                        "source": "LANDFIRE",
                        "product": product,
                        "version": version,
                        "interpolationMethod": interpolation_method,
                        "curingLiveHerbaceous": curing_live_herbaceous,
                        "curingLiveWoody": curing_live_woody,
                        "groups": groups,
                        "featureMasks": feature_masks,
                        "removeNonBurnable": remove_non_burnable,
                    }
                ).to_dict()
            )
        elif product == "FCCS":
            self.config["fuel_load"] = SurfaceGridLandfireFCCSFuelLoadSource.from_dict(
                {
                    "source": "LANDFIRE",
                    "product": product,
                    "version": version,
                    "interpolationMethod": interpolation_method,
                    "groups": groups,
                    "featureMasks": feature_masks,
                }
            ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELLOAD)

        return self

    def with_uniform_fuel_depth(
        self,
        value: float,
        feature_masks: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel depth value.

        Parameters
        ----------
        value : float
            Fuel depth in meters
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_depth(value=0.3, feature_masks=["road", "water"])
        """
        self.config["fuel_depth"] = Fueldepth.from_dict(
            {"source": "uniform", "value": value, "featureMasks": feature_masks}
        ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELDEPTH)

        return self

    def with_fuel_depth_from_landfire(
        self,
        product: str,
        version: str = "2022",
        interpolation_method: str = "nearest",
        feature_masks: list[str] = None,
        remove_non_burnable: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Configure fuel depth from LANDFIRE source.

        Parameters
        ----------
        product : str
            LANDFIRE product name ("FBFM40", "FBFM13", or "FCCS)
        version : str, optional
            LANDFIRE version, default "2022"
        interpolation_method : str, optional
            Method for interpolation, default "nearest"
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.
        remove_non_burnable : list[str], optional
            List of non-burnable fuel models to remove. This option is often used in conjunction with feature_masks to improve the resolution of landscape features. Can be: "NB1", "NB2", "NB3", "NB8", "NB9"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_fuel_depth_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest",
        ...     feature_masks=["road", "water"],
        ...     remove_non_burnable=["NB1", "NB2"]
        ... )
        """
        if product == "FBFM40":
            self.config["fuel_depth"] = SurfaceGridLandfireFBFM40Source.from_dict(
                {
                    "source": "LANDFIRE",
                    "product": product,
                    "version": version,
                    "interpolationMethod": interpolation_method,
                    "featureMasks": feature_masks,
                    "removeNonBurnable": remove_non_burnable,
                }
            ).to_dict()
        elif product == "FCCS":
            self.config["fuel_depth"] = SurfaceGridLandfireFCCSSource.from_dict(
                {
                    "source": "LANDFIRE",
                    "product": product,
                    "version": version,
                    "interpolationMethod": interpolation_method,
                    "featureMasks": feature_masks,
                }
            ).to_dict()
        self.attributes.append(SurfaceGridAttribute.FUELDEPTH)

        return self

    # Fuel Moisture Methods (only supports uniform)
    def with_uniform_fuel_moisture(
        self,
        value: float,
        feature_masks: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel moisture value.

        Parameters
        ----------
        value : float
            Fuel moisture value (%).
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_moisture(
        ...     value=15.0,  # 15%
        ...     feature_masks=["road", "water"]
        ... )
        """
        self.config["fuel_moisture"] = SurfaceGridFuelMoistureSource.from_dict(
            {"source": "uniform", "value": value, "featureMasks": feature_masks}
        ).to_dict()
        self.attributes.append("fuelMoisture")

        return self

    def with_uniform_fuel_moisture_by_size_class(
        self,
        one_hour: float = None,
        ten_hour: float = None,
        hundred_hour: float = None,
        live_herbaceous: float = None,
        live_woody: float = None,
        feature_masks: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform fuel moisture values by size class.

        Parameters
        ----------
        one_hour : float, optional
            1-hour fuel moisture content (%).
        ten_hour : float, optional
            10-hour fuel moisture content (%).
        hundred_hour : float, optional
            100-hour fuel moisture content (%).
        live_herbaceous : float, optional
            Live herbaceous fuel moisture content (%).
        live_woody : float, optional
            Live woody fuel moisture content (%).
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fuel_moisture_by_size_class(
        ...     one_hour=10.0,
        ...     ten_hour=15.0,
        ...     hundred_hour=20.0,
        ...     live_herbaceous=75.0,
        ...     live_woody=90.0,
        ...     feature_masks=["road", "water"]
        ... )
        """
        # Map parameter names to their corresponding group names in camelCase
        param_to_group = {
            "one_hour": "oneHour",
            "ten_hour": "tenHour",
            "hundred_hour": "hundredHour",
            "live_herbaceous": "liveHerbaceous",
            "live_woody": "liveWoody",
        }

        # Build the groups list based on which parameters have values
        groups = []
        for param_name, group_name in param_to_group.items():
            if locals()[param_name] is not None:
                groups.append(group_name)

        # Create the configuration dictionary
        self.config["fuel_moisture"] = SurfaceGridUniformValueBySizeClass.from_dict(
            {
                "source": "uniformBySizeClass",
                "oneHour": one_hour,
                "tenHour": ten_hour,
                "hundredHour": hundred_hour,
                "liveHerbaceous": live_herbaceous,
                "liveWoody": live_woody,
                "groups": groups,
                "featureMasks": feature_masks,
            }
        ).to_dict()
        self.attributes.append("fuelMoisture")

        return self

    def with_uniform_fbfm(
        self,
        value: str,
        feature_masks: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform Fire Behavior Fuel Model.

        Parameters
        ----------
        value : str
            FBFM value (e.g. "9", "GR2")
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_fbfm("GR2")
        """
        self.config["fbfm"] = SurfaceGridFBFMSource.from_dict(
            {"source": "uniform", "value": value, "featureMasks": feature_masks}
        ).to_dict()
        self.attributes.append("FBFM")

        return self

    def with_fbfm_from_landfire(
        self,
        product: str,
        version: str = "2022",
        interpolation_method: str = "nearest",
        feature_masks: list[str] = None,
        remove_non_burnable: list[str] = None,
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
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.
        remove_non_burnable : list[str], optional
            List of non-burnable fuel models to remove. This option is often used in conjunction with feature_masks to improve the resolution of landscape features. Can be: "NB1", "NB2", "NB3", "NB8", "NB9"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_fbfm_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest",
        ...     feature_masks=["road", "water"],
        ...     remove_non_burnable=["NB1", "NB2"]
        ... )
        """
        self.config["fbfm"] = SurfaceGridFBFMSource.from_dict(
            {
                "source": "LANDFIRE",
                "product": product,
                "version": version,
                "interpolationMethod": interpolation_method,
                "featureMasks": feature_masks,
                "removeNonBurnable": remove_non_burnable,
            }
        ).to_dict()
        self.attributes.append("FBFM")

        return self

    def with_uniform_savr(
        self,
        value: float,
        feature_masks: list[str] = None,
    ) -> "SurfaceGridBuilder":
        """Set uniform Surface Area to Volume Ratio (SAVR).

        Parameters
        ----------
        value : float
            SAVR value in m²/m³
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_uniform_savr(
        ...     value=9000, # m²/m³
        ...     feature_masks=["road", "water"]
        ... )
        """
        self.config["savr"] = SurfaceGridSAVRSource.from_dict(
            {"source": "uniform", "value": value, "featureMasks": feature_masks}
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
        feature_masks: list[str] = None,
        remove_non_burnable: list[str] = None,
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
        groups : list[str], optional
            List of SAVR groups to include. Can be: "oneHour", "tenHour", "hundredHour", "liveHerbaceous", "liveWoody"
        feature_masks : list[str], optional
            List of feature masks to apply to the surface grid attribute. Can be "road" or "water". Note that including these masks requires a feature grid with the appropriate attributes to have a "completed" status.
        remove_non_burnable : list[str], optional
            List of non-burnable fuel models to remove. This option is often used in conjunction with feature_masks to improve the resolution of landscape features. Can be: "NB1", "NB2", "NB3", "NB8", "NB9"

        Examples
        --------
        >>> builder = SurfaceGridBuilder("abc123")
        >>> builder.with_savr_from_landfire(
        ...     product="FBFM40",
        ...     version="2022",
        ...     interpolation_method="nearest",
        ...     groups=["oneHour", "tenHour", "hundredHour"],
        ...     feature_masks=["road", "water"],
        ...     remove_non_burnable=["NB1", "NB2"]
        ... )
        """
        self.config["savr"] = SurfaceGridLandfireFBFM40SAVRSource.from_dict(
            {
                "source": "LANDFIRE",
                "product": product,
                "version": version,
                "interpolationMethod": interpolation_method,
                "groups": groups,
                "featureMasks": feature_masks,
                "removeNonBurnable": remove_non_burnable,
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

    def with_spatial_modification(
        self,
        actions: (
            dict
            | list[dict]
            | SurfaceGridModificationAction
            | list[SurfaceGridModificationAction]
        ),
        geometry: dict,
        operator: str = "within",
        target: str = None,
        crs: dict = None,
        additional_conditions: (
            dict
            | list[dict]
            | SurfaceGridModificationCondition
            | list[SurfaceGridModificationCondition]
        ) = None,
    ) -> "SurfaceGridBuilder":
        """Add a spatial modification to the surface grid.

        Spatial modifications allow you to modify surface grid attributes based on
        geographic areas defined by GeoJSON geometries. This is useful for applying
        treatments to specific areas, such as reducing fuel load within a fuel break
        polygon or increasing moisture in riparian zones.

        Parameters
        ----------
        actions : dict or list[dict] or SurfaceGridModificationAction or list[SurfaceGridModificationAction]
            Action(s) to apply to cells matching the spatial condition.
        geometry : dict
            GeoJSON geometry (Polygon or MultiPolygon) defining the spatial area.
            Must include "type" and "coordinates" keys.
        operator : str, optional
            Spatial relationship to test. Options are:
            - "within": Select cells inside the geometry (default)
            - "outside": Select cells outside the geometry
            - "intersects": Select cells that overlap the geometry
        target : str, optional
            Which part of the cell to test against the geometry:
            - "centroid": Test the cell's center point (default)
            - "cell": Test the entire cell bounds
        crs : dict, optional
            Coordinate reference system for the geometry. If not specified,
            WGS84 (EPSG:4326) is assumed. Format: {"type": "name", "properties": {"name": "EPSG:XXXX"}}
        additional_conditions : dict or list[dict] or SurfaceGridModificationCondition or list[SurfaceGridModificationCondition], optional
            Additional attribute-based conditions to combine with the spatial condition.
            The modification will only apply to cells matching both the spatial and
            attribute conditions.

        Returns
        -------
        SurfaceGridBuilder
            Returns self for method chaining.

        Examples
        --------
        Reduce fuel load by 50% within a fuel break polygon:

        >>> builder = SurfaceGridBuilder("abc123")
        >>> fuel_break = {
        ...     "type": "Polygon",
        ...     "coordinates": [[[-120.5, 39.0], [-120.5, 39.1], [-120.4, 39.1], [-120.4, 39.0], [-120.5, 39.0]]]
        ... }
        >>> builder.with_spatial_modification(
        ...     actions={"attribute": "fuelLoad", "modifier": "multiply", "value": 0.5},
        ...     geometry=fuel_break,
        ...     operator="within"
        ... )

        Replace FBFM to non-burnable outside a study area:

        >>> study_area = {
        ...     "type": "Polygon",
        ...     "coordinates": [[[-120.5, 39.0], [-120.5, 39.5], [-120.0, 39.5], [-120.0, 39.0], [-120.5, 39.0]]]
        ... }
        >>> builder.with_spatial_modification(
        ...     actions={"attribute": "FBFM", "modifier": "replace", "value": "NB1"},
        ...     geometry=study_area,
        ...     operator="outside"
        ... )

        Increase fuel moisture in specific areas with UTM coordinates:

        >>> riparian_zone = {
        ...     "type": "Polygon",
        ...     "coordinates": [[[500000, 4300000], [500000, 4301000], [501000, 4301000], [501000, 4300000], [500000, 4300000]]]
        ... }
        >>> builder.with_spatial_modification(
        ...     actions={"attribute": "fuelMoisture", "modifier": "multiply", "value": 1.5},
        ...     geometry=riparian_zone,
        ...     operator="within",
        ...     crs={"type": "name", "properties": {"name": "EPSG:32610"}}
        ... )

        Combine spatial and attribute conditions:

        >>> builder.with_spatial_modification(
        ...     actions={"attribute": "fuelLoad", "modifier": "multiply", "value": 0.3},
        ...     geometry=fuel_break,
        ...     operator="within",
        ...     additional_conditions={"attribute": "FBFM", "operator": "eq", "value": "GR2"}
        ... )  # Only reduces fuel load for GR2 cells within the fuel break
        """
        # Build the spatial condition
        spatial_condition = {
            "operator": operator,
            "geometry": geometry,
        }
        if target is not None:
            spatial_condition["target"] = target
        if crs is not None:
            spatial_condition["crs"] = crs

        # Combine spatial condition with any additional attribute conditions
        conditions = [spatial_condition]
        if additional_conditions is not None:
            if isinstance(additional_conditions, list):
                conditions.extend(additional_conditions)
            else:
                conditions.append(additional_conditions)

        return self.with_modification(actions=actions, conditions=conditions)

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
