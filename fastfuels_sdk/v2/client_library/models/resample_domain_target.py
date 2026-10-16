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

from ..models.resampling_method import ResamplingMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResampleDomainTarget")


@_attrs_define
class ResampleDomainTarget:
    """Anchor output to the domain origin at the given cell size.

    Attributes:
        resolution (float):
        target (Literal['domain'] | Unset):  Default: 'domain'.
        method (None | ResamplingMethod | Unset):
    """

    resolution: float
    target: Literal["domain"] | Unset = "domain"
    method: None | ResamplingMethod | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resolution = self.resolution

        target = self.target

        method: None | str | Unset
        if isinstance(self.method, Unset):
            method = UNSET
        elif isinstance(self.method, ResamplingMethod):
            method = self.method.value
        else:
            method = self.method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resolution": resolution,
            }
        )
        if target is not UNSET:
            field_dict["target"] = target
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        resolution = d.pop("resolution")

        target = cast(Literal["domain"] | Unset, d.pop("target", UNSET))
        if target != "domain" and not isinstance(target, Unset):
            raise ValueError(f"target must match const 'domain', got '{target}'")

        def _parse_method(data: object) -> None | ResamplingMethod | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                method_type_0 = ResamplingMethod(data)

                return method_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ResamplingMethod | Unset, data)

        method = _parse_method(d.pop("method", UNSET))

        resample_domain_target = cls(
            resolution=resolution,
            target=target,
            method=method,
        )

        resample_domain_target.additional_properties = d
        return resample_domain_target

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
