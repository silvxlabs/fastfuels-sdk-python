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

T = TypeVar("T", bound="GridAlignmentDomainTarget")


@_attrs_define
class GridAlignmentDomainTarget:
    """Anchor output to the domain origin.

    `resolution=None` uses the source's native cell size. Output cells tile
    the domain bounding box (already snapped at domain creation if
    `pad_to_resolution` was set).

        Attributes:
            target (Literal['domain'] | Unset):  Default: 'domain'.
            resolution (float | None | Unset):
            method (None | ResamplingMethod | Unset):
    """

    target: Literal["domain"] | Unset = "domain"
    resolution: float | None | Unset = UNSET
    method: None | ResamplingMethod | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        resolution: float | None | Unset
        if isinstance(self.resolution, Unset):
            resolution = UNSET
        else:
            resolution = self.resolution

        method: None | str | Unset
        if isinstance(self.method, Unset):
            method = UNSET
        elif isinstance(self.method, ResamplingMethod):
            method = self.method.value
        else:
            method = self.method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target is not UNSET:
            field_dict["target"] = target
        if resolution is not UNSET:
            field_dict["resolution"] = resolution
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        target = cast(Literal["domain"] | Unset, d.pop("target", UNSET))
        if target != "domain" and not isinstance(target, Unset):
            raise ValueError(f"target must match const 'domain', got '{target}'")

        def _parse_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        resolution = _parse_resolution(d.pop("resolution", UNSET))

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

        grid_alignment_domain_target = cls(
            target=target,
            resolution=resolution,
            method=method,
        )

        grid_alignment_domain_target.additional_properties = d
        return grid_alignment_domain_target

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
