from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoveAction")


@_attrs_define
class RemoveAction:
    """Action that removes matching trees from the inventory.

    Attributes:
        modifier (Literal['remove'] | Unset):  Default: 'remove'.
    """

    modifier: Literal["remove"] | Unset = "remove"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        modifier = self.modifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if modifier is not UNSET:
            field_dict["modifier"] = modifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        modifier = cast(Literal["remove"] | Unset, d.pop("modifier", UNSET))
        if modifier != "remove" and not isinstance(modifier, Unset):
            raise ValueError(f"modifier must match const 'remove', got '{modifier}'")

        remove_action = cls(
            modifier=modifier,
        )

        remove_action.additional_properties = d
        return remove_action

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
