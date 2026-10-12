from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chm_crown_segmentation import ChmCrownSegmentation


T = TypeVar("T", bound="CreateChmCrownFeatureRequest")


@_attrs_define
class CreateChmCrownFeatureRequest:
    """Request body for creating a crown feature from a CHM.

    Attributes:
        source_inventory_id (str): ID of a completed tree inventory in this domain, created with `POST
            /inventories/tree/chm` from `source_chm_grid_id`. Each tree seeds one crown at its `x`, `y`.
        source_chm_grid_id (str): ID of a completed grid in this domain with a `chm` band in metres, at 2 m resolution
            or finer.
        type_ (Literal['crown'] | Unset):  Default: 'crown'.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        crown_segmentation (ChmCrownSegmentation | Unset): Crown segmentation settings for a crown Feature.

            When set, ``max_height`` must be greater than ``min_height``.
    """

    source_inventory_id: str
    source_chm_grid_id: str
    type_: Literal["crown"] | Unset = "crown"
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    crown_segmentation: ChmCrownSegmentation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_inventory_id = self.source_inventory_id

        source_chm_grid_id = self.source_chm_grid_id

        type_ = self.type_

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        crown_segmentation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.crown_segmentation, Unset):
            crown_segmentation = self.crown_segmentation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_inventory_id": source_inventory_id,
                "source_chm_grid_id": source_chm_grid_id,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if crown_segmentation is not UNSET:
            field_dict["crown_segmentation"] = crown_segmentation

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.chm_crown_segmentation import ChmCrownSegmentation

        d = dict(src_dict)
        source_inventory_id = d.pop("source_inventory_id")

        source_chm_grid_id = d.pop("source_chm_grid_id")

        type_ = cast(Literal["crown"] | Unset, d.pop("type", UNSET))
        if type_ != "crown" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'crown', got '{type_}'")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _crown_segmentation = d.pop("crown_segmentation", UNSET)
        crown_segmentation: ChmCrownSegmentation | Unset
        if isinstance(_crown_segmentation, Unset):
            crown_segmentation = UNSET
        else:
            crown_segmentation = ChmCrownSegmentation.from_dict(_crown_segmentation)

        create_chm_crown_feature_request = cls(
            source_inventory_id=source_inventory_id,
            source_chm_grid_id=source_chm_grid_id,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            crown_segmentation=crown_segmentation,
        )

        create_chm_crown_feature_request.additional_properties = d
        return create_chm_crown_feature_request

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
