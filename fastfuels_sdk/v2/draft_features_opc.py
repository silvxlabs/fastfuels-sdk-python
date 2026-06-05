"""
fastfuels_sdk/v2/draft_features_opc.py

DRAFT — Feature wrapper built on the **openapi-python-client** client
(`client_library`: attrs models + httpx).

Part of the v2 client-library generator comparison; see COMPARISON.md.
Covers OSM road and water feature creation plus the get/wait/update/
delete/list lifecycle.
"""

import json
import time
from typing import Any, List, Optional

import attrs

from fastfuels_sdk.v2.api import ensure_client as get_client
from fastfuels_sdk.v2.draft_grids_opc import _checked

from fastfuels_sdk.v2.client_library.api.features import (
    create_osm_road_feature,
    create_osm_water_feature,
    delete_feature,
    get_feature,
    list_features as list_features_endpoint,
    update_feature,
)
from fastfuels_sdk.v2.client_library.models import (
    Feature as FeatureModel,
    CreateOsmRoadFeatureRequest,
    CreateOsmWaterFeatureRequest,
    JobStatus,
    ListFeaturesResponse,
    UpdateFeatureRequestBody,
)
from fastfuels_sdk.v2.client_library.types import UNSET


def _osm_request_dict(
    name: str,
    description: str,
    tags: Optional[List[str]],
    extent_buffer_m: float,
) -> dict:
    """Build the request fields shared by the OSM feature endpoints."""
    body: dict[str, Any] = {
        "name": name,
        "description": description,
        "extent_buffer_m": extent_buffer_m,
    }
    if tags is not None:
        body["tags"] = tags
    return body


class Feature(FeatureModel):
    """Feature resource for the FastFuels v2 API (openapi-python-client draft).

    Inherits all attributes from the generated attrs model: id, domain_id,
    type_, name, description, status, progress, source, georeference,
    error, tags, created_on, modified_on.

    v2 unifies road and water features (separate sub-resources in v1) into
    one job-based Feature resource distinguished by its `type_`/`source`.
    """

    @classmethod
    def _from_model(cls, model: FeatureModel) -> "Feature":
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: FeatureModel) -> "Feature":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(FeatureModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    @classmethod
    def from_id(cls, domain_id: str, feature_id: str) -> "Feature":
        """Retrieve an existing Feature by domain and feature ID."""
        response = get_feature.sync(domain_id, feature_id, client=get_client())
        return cls._from_model(_checked(response, FeatureModel))

    @classmethod
    def create_osm_road(
        cls,
        domain_id: str,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        extent_buffer_m: float = 0,
    ) -> "Feature":
        """Create a road feature from OpenStreetMap data."""
        body = _osm_request_dict(name, description, tags, extent_buffer_m)
        request = CreateOsmRoadFeatureRequest.from_dict(body)
        response = create_osm_road_feature.sync(
            domain_id, client=get_client(), body=request
        )
        return cls._from_model(_checked(response, FeatureModel))

    @classmethod
    def create_osm_water(
        cls,
        domain_id: str,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        extent_buffer_m: float = 0,
    ) -> "Feature":
        """Create a water feature from OpenStreetMap data."""
        body = _osm_request_dict(name, description, tags, extent_buffer_m)
        request = CreateOsmWaterFeatureRequest.from_dict(body)
        response = create_osm_water_feature.sync(
            domain_id, client=get_client(), body=request
        )
        return cls._from_model(_checked(response, FeatureModel))

    def get(self, in_place: bool = False) -> "Feature":
        """Retrieve the latest feature data from the API."""
        response = _checked(
            get_feature.sync(self.domain_id, self.id, client=get_client()),
            FeatureModel,
        )
        if in_place:
            return self._copy_fields_from(response)
        return Feature._from_model(response)

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> "Feature":
        """Poll the feature job until it reaches a terminal status."""
        elapsed = 0.0
        feature = self.get()
        while feature.status not in (JobStatus.COMPLETED, JobStatus.FAILED):
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Feature {self.id} did not complete within {timeout} seconds"
                )
            time.sleep(step)
            elapsed += step
            feature = self.get()
            if verbose:
                print(f"Feature {self.id}: {feature.status} ({elapsed:.0f}s)")
        if feature.status == JobStatus.FAILED:
            raise RuntimeError(f"Feature {self.id} failed: {feature.error}")
        if in_place:
            return self._copy_fields_from(feature)
        return feature

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        in_place: bool = False,
    ) -> "Feature":
        """Update the feature's mutable properties (name, description, tags)."""
        if name is None and description is None and tags is None:
            return self if in_place else Feature._from_model(self)
        request = UpdateFeatureRequestBody(
            name=name if name is not None else UNSET,
            description=description if description is not None else UNSET,
            tags=tags if tags is not None else UNSET,
        )
        response = _checked(
            update_feature.sync(
                self.domain_id, self.id, client=get_client(), body=request
            ),
            FeatureModel,
        )
        if in_place:
            return self._copy_fields_from(response)
        return Feature._from_model(response)

    def delete(self) -> None:
        """Delete this feature."""
        delete_feature.sync_detailed(self.domain_id, self.id, client=get_client())

    def to_json(self) -> str:
        """Serialize the complete Feature object to a JSON string."""
        return json.dumps(self.to_dict(), default=str, indent=2)


def list_features(
    domain_id: str,
    page: int = 0,
    size: int = 100,
) -> List[Feature]:
    """List features in a domain (single page)."""
    response = _checked(
        list_features_endpoint.sync(
            domain_id, client=get_client(), page=page, size=size
        ),
        ListFeaturesResponse,
    )
    return [Feature._from_model(f) for f in response.features]
