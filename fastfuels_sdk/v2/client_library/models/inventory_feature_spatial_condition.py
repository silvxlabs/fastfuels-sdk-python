from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.spatial_operator import SpatialOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryFeatureSpatialCondition")


@_attrs_define
class InventoryFeatureSpatialCondition:
    """Spatial condition that tests tree locations against a persisted Feature
    resource.

    The referenced Feature must belong to the same domain as the inventory.
    The processing service loads the feature's geometry, reprojects it into
    the domain CRS, optionally buffers it, and then evaluates the spatial
    operator against each tree's point coordinate.

    A non-zero ``buffer_m`` is typically required for linestring features
    (e.g. roads), since tree points almost never intersect a bare linestring.

        Attributes:
            source (Literal['feature']): Discriminator selecting this variant. Must be the literal string `"feature"`. Use
                `"geometry"` instead to supply inline GeoJSON.
            operator (SpatialOperator): Spatial relationship operators for geometry-based conditions.

                - within: Select items whose target (centroid or cell) is inside the geometry
                - outside: Select items whose target is outside the geometry (inverse of within)
                - intersects: Select items whose target overlaps with the geometry
            feature_id (str): ID of a Feature resource (road, water, or layerset) hosted in the same domain as the
                inventory. Cross-domain references are rejected; the feature must be in `completed` status.
            buffer_m (float | None | Unset): Optional buffer distance in meters applied to the feature geometry (in the
                domain's projected CRS) before testing. Effectively required for linestring features such as roads since a tree
                point almost never intersects a bare linestring.
    """

    source: Literal["feature"]
    operator: SpatialOperator
    feature_id: str
    buffer_m: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        operator = self.operator.value

        feature_id = self.feature_id

        buffer_m: float | None | Unset
        if isinstance(self.buffer_m, Unset):
            buffer_m = UNSET
        else:
            buffer_m = self.buffer_m

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "operator": operator,
                "feature_id": feature_id,
            }
        )
        if buffer_m is not UNSET:
            field_dict["buffer_m"] = buffer_m

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source = cast(Literal["feature"], d.pop("source"))
        if source != "feature":
            raise ValueError(f"source must match const 'feature', got '{source}'")

        operator = SpatialOperator(d.pop("operator"))

        feature_id = d.pop("feature_id")

        def _parse_buffer_m(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        buffer_m = _parse_buffer_m(d.pop("buffer_m", UNSET))

        inventory_feature_spatial_condition = cls(
            source=source,
            operator=operator,
            feature_id=feature_id,
            buffer_m=buffer_m,
        )

        inventory_feature_spatial_condition.additional_properties = d
        return inventory_feature_spatial_condition

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
