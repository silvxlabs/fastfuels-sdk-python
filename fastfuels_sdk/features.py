"""
fastfuels_sdk/features.py
"""

# Core imports
from __future__ import annotations
from time import sleep
from typing import Optional, List, Union, Dict, Any

# Internal imports
from fastfuels_sdk.api import (
    get_features_api,
    get_road_feature_api,
    get_water_feature_api,
)
from fastfuels_sdk.utils import format_processing_error
from fastfuels_sdk.client_library.models import (
    Features as FeaturesModel,
    RoadFeature as RoadFeatureModel,
    WaterFeature as WaterFeatureModel,
    CreateRoadFeatureRequest,
    CreateWaterFeatureRequest,
    RoadFeatureSource,
    WaterFeatureSource,
    Geojson,
)


class Features(FeaturesModel):
    """Geographic features (roads and water bodies) associated with a domain.

    Attributes
    ----------
    domain_id : str
        ID of the domain these features belong to
    road : RoadFeature, optional
        Road network data
    water : WaterFeature, optional
        Water body data

    Examples
    --------
    >>> from fastfuels_sdk import Features
    >>> features = Features.from_domain_id("abc123")

    >>> # Access road data
    >>> if features.road:
    ...     roads = features.road

    >>> # Access water data
    >>> if features.water:
    ...     water = features.water

    >>> # Get updated feature data
    >>> features = features.get()

    See Also
    --------
    Domain : Container for features
    RoadFeature : Road network structure
    WaterFeature : Water body structure
    """

    domain_id: str
    road: Optional[RoadFeature]
    water: Optional[WaterFeature]

    @classmethod
    def from_domain_id(cls, domain_id: str) -> Features:
        """Retrieve the features (roads and water bodies) associated with a domain.

        Parameters
        ----------
        domain_id : str
            The ID of the domain to retrieve features for

        Returns
        -------
        Features
            A Features object containing:
            - road : RoadFeature, optional
                Road network data within the domain
            - water : WaterFeature, optional
                Water bodies within the domain

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")

        >>> # Check for specific features. These will be None until created.
        >>> if features.road:
        ...     print("Domain has road features")
        >>> if features.water:
        ...     print("Domain has water features")

        See Also
        --------
        Features.get : Refresh feature data
        """
        features_response = get_features_api().get_features(domain_id=domain_id)
        response_data = _convert_api_models_to_sdk_classes(
            domain_id, features_response.model_dump(), features_response
        )

        return cls(domain_id=domain_id, **response_data)

    def get(self, in_place: bool = False) -> Features:
        """Get the latest feature data for this domain.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this Features instance with new data.
            If False (default), returns a new Features instance.

        Returns
        -------
        Features
            The updated Features object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> # Get fresh data in a new instance
        >>> updated_features = features.get()
        >>>
        >>> # Or update the existing instance
        >>> features.get(in_place=True)

        See Also
        --------
        Features.from_domain : Get features for a specific domain
        """
        response = get_features_api().get_features(domain_id=self.domain_id)
        response_data = response.model_dump()
        response_data = _convert_api_models_to_sdk_classes(
            self.domain_id, response_data, response
        )

        if in_place:
            # Update all attributes of current instance
            for key, value in response_data.items():
                setattr(self, key, value)
            return self

        return Features(domain_id=self.domain_id, **response_data)

    def create_road_feature(
        self,
        sources: str | List[str] | RoadFeatureSource | List[RoadFeatureSource],
        geojson: Optional[Union[Dict[str, Any], Geojson]] = None,
        in_place: bool = False,
    ) -> RoadFeature:
        """Create road features for this domain using specified data sources.

        Parameters
        ----------
        sources : str or list[str] or RoadFeatureSource or list[RoadFeatureSource]
            Data sources to use. Supports:
            - "OSM": OpenStreetMap data (not supported for local CRS domains)
            - "geojson": User-provided GeoJSON data (supported for all CRS including local)
        geojson : dict or Geojson, optional
            GeoJSON Feature or FeatureCollection containing Polygon or MultiPolygon geometries.
            Required when source is "geojson".
        in_place : bool, optional
            If True, updates this Features instance with new data.
            If False (default), leaves this instance unchanged.

        Returns
        -------
        RoadFeature
            The newly created road feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> # Create from OpenStreetMap
        >>> road = features.create_road_feature("OSM")
        >>>
        >>> # Create from GeoJSON
        >>> geojson_data = {
        ...     "type": "FeatureCollection",
        ...     "features": [{
        ...         "type": "Feature",
        ...         "geometry": {
        ...             "type": "Polygon",
        ...             "coordinates": [[...]]
        ...         }
        ...     }]
        ... }
        >>> road = features.create_road_feature("geojson", geojson=geojson_data)
        >>>
        >>> # Update Features instance
        >>> features.create_road_feature("OSM", in_place=True)
        >>> features.road.status
        "pending"

        See Also
        --------
        Features.create_road_feature_from_osm : Simpler method for OSM data
        Features.create_road_feature_from_geodataframe : Simpler method for GeoDataFrame data
        """
        # Normalize sources to list
        sources_list = [sources] if isinstance(sources, str) else sources

        # Convert geojson dict to Geojson model if needed
        geojson_param = None
        if geojson is not None:
            if isinstance(geojson, dict):
                geojson_param = Geojson.from_dict(geojson)
            else:
                geojson_param = geojson

        # Create API request
        request = CreateRoadFeatureRequest(sources=sources_list, geojson=geojson_param)

        # Call API
        response = get_road_feature_api().create_road_feature(
            domain_id=self.domain_id, create_road_feature_request=request
        )

        # Convert API model to SDK class
        # Keep the geojson field as-is since it's already a Geojson instance
        response_dict = response.model_dump()
        # The geojson field from response is already a Geojson instance, keep it
        if hasattr(response, "geojson") and response.geojson is not None:
            response_dict["geojson"] = response.geojson

        road_feature = RoadFeature(domain_id=self.domain_id, **response_dict)

        if in_place:
            self.road = road_feature

        return road_feature

    def create_road_feature_from_osm(self, in_place: bool = False) -> RoadFeature:
        """Create road features for this domain using OpenStreetMap data.

        This is a convenience method that provides a simpler interface for the
        common case of using OpenStreetMap as the data source.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this Features instance with new data.
            If False (default), leaves this instance unchanged.

        Returns
        -------
        RoadFeature
            The newly created road feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> # Create new road features
        >>> road = features.create_road_feature_from_osm()
        >>>
        >>> # Update Features instance
        >>> features.create_road_feature_from_osm(in_place=True)
        >>> features.road.status
        "pending"

        See Also
        --------
        Features.create_road_feature : More general method supporting multiple sources
        """
        return self.create_road_feature(sources="OSM", in_place=in_place)

    def create_road_feature_from_geodataframe(
        self,
        gdf,
        in_place: bool = False,
    ) -> RoadFeature:
        """Create road features for this domain from a GeoPandas GeoDataFrame.

        This convenience method accepts a GeoDataFrame and converts it to GeoJSON
        for road feature creation. Supports all coordinate systems including local CRS.

        Parameters
        ----------
        gdf : geopandas.GeoDataFrame
            GeoDataFrame containing Polygon or MultiPolygon geometries representing road areas.
            The geometries will be clipped to the domain boundary.
        in_place : bool, optional
            If True, updates this Features instance with new data.
            If False (default), leaves this instance unchanged.

        Returns
        -------
        RoadFeature
            The newly created road feature object

        Examples
        --------
        >>> import geopandas as gpd
        >>> from shapely.geometry import Polygon
        >>> from fastfuels_sdk import Features
        >>>
        >>> features = Features.from_domain_id("abc123")
        >>>
        >>> # Create GeoDataFrame with road polygons
        >>> gdf = gpd.GeoDataFrame({
        ...     'geometry': [Polygon([
        ...         (-120.0, 39.0),
        ...         (-120.0, 39.1),
        ...         (-119.9, 39.1),
        ...         (-119.9, 39.0),
        ...         (-120.0, 39.0)
        ...     ])]
        ... }, crs="EPSG:4326")
        >>>
        >>> # Create road features
        >>> road = features.create_road_feature_from_geodataframe(gdf)
        >>>
        >>> # Update Features instance
        >>> features.create_road_feature_from_geodataframe(gdf, in_place=True)
        >>> features.road.status
        "pending"

        See Also
        --------
        Features.create_road_feature : More general method supporting multiple sources
        Features.create_road_feature_from_osm : Simpler method for OSM data
        """
        import json

        # Convert GeoDataFrame to GeoJSON dict
        geojson_str = gdf.to_json()
        geojson_dict = json.loads(geojson_str)

        return self.create_road_feature(
            sources="geojson", geojson=geojson_dict, in_place=in_place
        )

    def create_water_feature(
        self,
        sources: str | List[str] | WaterFeatureSource | List[WaterFeatureSource],
        in_place: bool = False,
    ) -> WaterFeature:
        """Create water features for this domain using specified data sources.

        Parameters
        ----------
        sources : str or list[str] or WaterFeatureSource or list[WaterFeatureSource]
            Data sources to use. Currently, supports:
            - "OSM": OpenStreetMap data
        in_place : bool, optional
            If True, updates this Features instance with new data.
            If False (default), leaves this instance unchanged.

        Returns
        -------
        WaterFeature
            The newly created water feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>>
        >>> # Create from OpenStreetMap
        >>> water = features.create_water_feature("OSM")
        >>>
        >>> # Update Features instance
        >>> features.create_water_feature("OSM", in_place=True)
        >>> features.water.status
        "pending"

        See Also
        --------
        Features.create_water_feature_from_osm : Simpler method for OSM data
        """
        # Create API request
        request = CreateWaterFeatureRequest(
            sources=[sources] if isinstance(sources, str) else sources
        )

        # Call API
        response = get_water_feature_api().create_water_feature(
            domain_id=self.domain_id, create_water_feature_request=request
        )

        # Convert API model to SDK class
        water_feature = WaterFeature(domain_id=self.domain_id, **response.model_dump())

        if in_place:
            self.water = water_feature

        return water_feature

    def create_water_feature_from_osm(self, in_place: bool = False) -> WaterFeature:
        """Create water features for this domain using OpenStreetMap data.

        This is a convenience method that provides a simpler interface for the
        common case of using OpenStreetMap as the data source.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this Features instance with new data.
            If False (default), leaves this instance unchanged.

        Returns
        -------
        WaterFeature
            The newly created water feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>>
        >>> # Create new water features
        >>> water = features.create_water_feature_from_osm()
        >>>
        >>> # Update Features instance with new water feature
        >>> features.create_water_feature_from_osm(in_place=True)
        >>> features.water.status
        "pending"

        See Also
        --------
        Features.create_water_feature : More general method supporting multiple sources
        """
        return self.create_water_feature(sources="OSM", in_place=in_place)


class RoadFeature(RoadFeatureModel):
    """Road network features within a domain's spatial boundaries.

    Represents road features extracted from various data sources (OpenStreetMap
    or user-provided GeoJSON/GeoDataFrame). Road features include information about
    road locations, types, and attributes.

    Attributes
    ----------
    domain_id : str
        ID of the domain these roads belong to
    sources : list[RoadFeatureSource]
        Data sources used to create these features ("OSM" or "geojson")
    geojson : Geojson, optional
        GeoJSON data if created from geojson source
    status : str, optional
        Current processing status ("pending", "running", "completed")
    created_on : datetime, optional
        When these features were created
    modified_on : datetime, optional
        When these features were last modified
    checksum : str, optional
        Unique identifier for this version of the features

    Examples
    --------
    >>> from fastfuels_sdk.features import Features
    Get existing road features:
    >>> features = Features.from_domain_id("abc123")
    >>> if features.road:
    ...     road_features = features.road

    Create road features from OpenStreetMap:
    >>> road_features = features.create_road_feature("OSM")
    >>> print(road_features.status)
    'pending'

    Create road features from GeoDataFrame:
    >>> import geopandas as gpd
    >>> gdf = gpd.read_file("roads.geojson")
    >>> road_features = features.create_road_feature_from_geodataframe(gdf)
    """

    domain_id: str

    def get(self, in_place: bool = False) -> RoadFeature:
        """Get the latest road feature data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this RoadFeature instance with new data.
            If False (default), returns a new RoadFeature instance.

        Returns
        -------
        RoadFeature
            The updated road feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> road = features.create_road_feature("OSM")
        >>> # Get fresh data in a new instance
        >>> updated_road = road.get()
        >>>
        >>> # Or update the existing instance
        >>> road.get(in_place=True)
        """
        response = get_road_feature_api().get_road_feature(domain_id=self.domain_id)
        response_dict = response.model_dump()

        # The geojson field from response is already a Geojson instance, keep it
        if hasattr(response, "geojson") and response.geojson is not None:
            response_dict["geojson"] = response.geojson

        if in_place:
            # Update all attributes of current instance
            for key, value in response_dict.items():
                setattr(self, key, value)
            return self
        return RoadFeature(domain_id=self.domain_id, **response_dict)

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> RoadFeature:
        """Wait for road feature processing to complete.

        Road features are processed asynchronously and may take several seconds to
        minutes to complete depending on domain size and data sources.

        Parameters
        ----------
        step : float, optional
            Seconds between status checks (default: 5)
        timeout : float, optional
            Maximum seconds to wait (default: 600)
        in_place : bool, optional
            If True (default), updates this instance with completed data.
            If False, returns a new instance.
        verbose : bool, optional
            If True, prints status updates (default: False)

        Returns
        -------
        RoadFeature
            The completed road feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> road = features.create_road_feature("OSM")
        >>> road.wait_until_completed(verbose=True)
        Road features have status `pending` (5.00s)
        Road features have status `completed` (10.00s)
        """
        elapsed_time = 0
        road_feature = self.get(in_place=in_place if in_place else False)
        while road_feature.status != "completed":
            if road_feature.status == "failed":
                error_msg = "Road feature processing failed."

                # Extract detailed error information if available
                error_obj = getattr(road_feature, "error", None)
                if error_obj:
                    error_details = format_processing_error(error_obj)
                    if error_details:
                        error_msg = f"{error_msg}\n\n{error_details}"

                raise RuntimeError(error_msg)
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for road features to finish.")
            sleep(step)
            elapsed_time += step
            road_feature = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(
                    f"Road features have status `{road_feature.status}` ({elapsed_time:.2f}s)"
                )
        return road_feature

    def delete(self) -> None:
        """Delete these road features.

        Permanently removes road feature data from the domain. This also cancels
        any ongoing processing jobs.

        Returns
        -------
        None

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> road = features.create_road_feature("OSM")
        >>> # Remove road features when no longer needed
        >>> road.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> road.get()  # raises NotFoundException
        """
        get_road_feature_api().delete_road_feature(domain_id=self.domain_id)
        return None


class WaterFeature(WaterFeatureModel):
    """Water body features within a domain's spatial boundaries.

    Represents water features extracted from various data sources (like OpenStreetMap)
    within a domain. Water features include information about water body locations,
    types, and attributes.

    Attributes
    ----------
    domain_id : str
        ID of the domain these water bodies belong to
    sources : list[WaterFeatureSource]
        Data sources used to create these features
    status : str, optional
        Current processing status ("pending", "running", "completed")
    created_on : datetime, optional
        When these features were created
    modified_on : datetime, optional
        When these features were last modified
    checksum : str, optional
        Unique identifier for this version of the features

    Examples
    --------
    Get existing water features:
    >>> from fastfuels_sdk import Features
    >>> features = Features.from_domain_id("abc123")
    >>> if features.water:
    ...     water_features = features.water

    Create new water features:
    >>> water_features = features.create_water_feature("OSM")
    >>> print(water_features.status)
    'pending'
    """

    domain_id: str

    def get(self, in_place: bool = False) -> WaterFeature:
        """Get the latest water feature data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this WaterFeature instance with new data.
            If False (default), returns a new WaterFeature instance.

        Returns
        -------
        WaterFeature
            The updated water feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> water = features.create_water_feature("OSM")
        >>> # Get fresh data in a new instance
        >>> updated_water = water.get()
        >>>
        >>> # Or update the existing instance
        >>> water.get(in_place=True)
        """
        response = get_water_feature_api().get_water_feature(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return WaterFeature(domain_id=self.domain_id, **response.model_dump())

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> WaterFeature:
        """Wait for water feature processing to complete.

        Water features are processed asynchronously and may take several seconds to
        minutes to complete depending on domain size and data sources.

        Parameters
        ----------
        step : float, optional
            Seconds between status checks (default: 5)
        timeout : float, optional
            Maximum seconds to wait (default: 600)
        in_place : bool, optional
            If True (default), updates this instance with completed data.
            If False, returns a new instance.
        verbose : bool, optional
            If True, prints status updates (default: False)

        Returns
        -------
        WaterFeature
            The completed water feature object

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> water = features.create_water_feature("OSM")
        >>> water.wait_until_completed(verbose=True)
        Water features have status `pending` (5.00s)
        Water features have status `completed` (10.00s)
        """
        elapsed_time = 0
        water_feature = self.get(in_place=in_place if in_place else False)
        while water_feature.status != "completed":
            if water_feature.status == "failed":
                error_msg = "Water feature processing failed."

                # Extract detailed error information if available
                # Check for error in multiple possible locations
                error_obj = getattr(water_feature, "error", None)
                if error_obj:
                    error_details = format_processing_error(error_obj)
                    if error_details:
                        error_msg = f"{error_msg}\n\n{error_details}"

                raise RuntimeError(error_msg)
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for water features to finish.")
            sleep(step)
            elapsed_time += step
            water_feature = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(
                    f"Water features have status `{water_feature.status}` ({elapsed_time:.2f}s)"
                )
        return water_feature

    def delete(self) -> None:
        """Delete these water features.

        Permanently removes water feature data from the domain. This also cancels
        any ongoing processing jobs.

        Returns
        -------
        None

        Examples
        --------
        >>> from fastfuels_sdk import Features
        >>> features = Features.from_domain_id("abc123")
        >>> water = features.create_water_feature("OSM")
        >>> # Remove water features when no longer needed
        >>> water.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> water.get()  # raises NotFoundException
        """
        get_water_feature_api().delete_water_feature(domain_id=self.domain_id)
        return None


def _convert_api_models_to_sdk_classes(
    domain_id, response_data: dict, response_obj=None
) -> dict:
    """Convert API models to SDK classes with domain_id.

    Parameters
    ----------
    domain_id : str
        Domain ID to attach to features
    response_data : dict
        Dict representation of the response
    response_obj : optional
        Original response object (to preserve complex nested models like Geojson)
    """
    if "road" in response_data and response_data["road"]:
        road_data = response_data["road"]
        # If we have the original response object, use its geojson field directly
        if response_obj and hasattr(response_obj, "road") and response_obj.road:
            if (
                hasattr(response_obj.road, "geojson")
                and response_obj.road.geojson is not None
            ):
                road_data["geojson"] = response_obj.road.geojson
        response_data["road"] = RoadFeature(domain_id=domain_id, **road_data)
    if "water" in response_data and response_data["water"]:
        response_data["water"] = WaterFeature(
            domain_id=domain_id, **response_data["water"]
        )

    return response_data
