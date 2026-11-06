from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConcatenateFeaturesRequest")


@_attrs_define
class ConcatenateFeaturesRequest:
    """Request body for concatenating features of one type.

    Attributes:
        source_feature_ids (list[str]): IDs of the features to combine, in the order their rows are appended. Each must
            be a completed feature of the path's type in this domain, and listed once.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
    """

    source_feature_ids: list[str]
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_feature_ids = self.source_feature_ids

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_feature_ids": source_feature_ids,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        source_feature_ids = cast(list[str], d.pop("source_feature_ids"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        concatenate_features_request = cls(
            source_feature_ids=source_feature_ids,
            name=name,
            description=description,
            tags=tags,
        )

        concatenate_features_request.additional_properties = d
        return concatenate_features_request

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
