from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.resampling_method import ResamplingMethod

T = TypeVar("T", bound="CreateResampleRequestMethodOverrides")


@_attrs_define
class CreateResampleRequestMethodOverrides:
    """Per-band resampling method overrides keyed by band key. Wins over ``alignment.method`` for the listed bands. Useful
    for using nearest-neighbor on categorical bands while using bilinear on continuous bands.

    """

    additional_properties: dict[str, ResamplingMethod] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        create_resample_request_method_overrides = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ResamplingMethod(prop_dict)

            additional_properties[prop_name] = additional_property

        create_resample_request_method_overrides.additional_properties = (
            additional_properties
        )
        return create_resample_request_method_overrides

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ResamplingMethod:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ResamplingMethod) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
