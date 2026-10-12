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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CrownFeatureCrownGeometrySource")


@_attrs_define
class CrownFeatureCrownGeometrySource:
    """Draw crowns from a crown Feature's footprints and its CHM.

    Attributes:
        feature_id (str): ID of a completed crown Feature in this domain.
        type_ (Literal['crown_feature'] | Unset):  Default: 'crown_feature'.
    """

    feature_id: str
    type_: Literal["crown_feature"] | Unset = "crown_feature"

    def to_dict(self) -> dict[str, Any]:
        feature_id = self.feature_id

        type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "feature_id": feature_id,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        feature_id = d.pop("feature_id")

        type_ = cast(Literal["crown_feature"] | Unset, d.pop("type", UNSET))
        if type_ != "crown_feature" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'crown_feature', got '{type_}'")

        crown_feature_crown_geometry_source = cls(
            feature_id=feature_id,
            type_=type_,
        )

        return crown_feature_crown_geometry_source
