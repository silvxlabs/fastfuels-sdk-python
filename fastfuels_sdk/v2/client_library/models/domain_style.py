from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DomainStyle")


@_attrs_define
class DomainStyle:
    """Optional visual style for rendering a domain on a map.

    All fields are optional. On PATCH only the provided fields are merged
    into the stored style; unspecified fields preserve their current values.

        Attributes:
            stroke_color (None | str | Unset): Stroke color in any renderer-supported format.
            stroke_opacity (float | None | Unset): Stroke opacity in [0, 1].
            stroke_width (float | None | Unset): Stroke width in pixels (non-negative).
            fill_color (None | str | Unset): Fill color in any renderer-supported format.
            fill_opacity (float | None | Unset): Fill opacity in [0, 1].
    """

    stroke_color: None | str | Unset = UNSET
    stroke_opacity: float | None | Unset = UNSET
    stroke_width: float | None | Unset = UNSET
    fill_color: None | str | Unset = UNSET
    fill_opacity: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stroke_color: None | str | Unset
        if isinstance(self.stroke_color, Unset):
            stroke_color = UNSET
        else:
            stroke_color = self.stroke_color

        stroke_opacity: float | None | Unset
        if isinstance(self.stroke_opacity, Unset):
            stroke_opacity = UNSET
        else:
            stroke_opacity = self.stroke_opacity

        stroke_width: float | None | Unset
        if isinstance(self.stroke_width, Unset):
            stroke_width = UNSET
        else:
            stroke_width = self.stroke_width

        fill_color: None | str | Unset
        if isinstance(self.fill_color, Unset):
            fill_color = UNSET
        else:
            fill_color = self.fill_color

        fill_opacity: float | None | Unset
        if isinstance(self.fill_opacity, Unset):
            fill_opacity = UNSET
        else:
            fill_opacity = self.fill_opacity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stroke_color is not UNSET:
            field_dict["stroke_color"] = stroke_color
        if stroke_opacity is not UNSET:
            field_dict["stroke_opacity"] = stroke_opacity
        if stroke_width is not UNSET:
            field_dict["stroke_width"] = stroke_width
        if fill_color is not UNSET:
            field_dict["fill_color"] = fill_color
        if fill_opacity is not UNSET:
            field_dict["fill_opacity"] = fill_opacity

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_stroke_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        stroke_color = _parse_stroke_color(d.pop("stroke_color", UNSET))

        def _parse_stroke_opacity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        stroke_opacity = _parse_stroke_opacity(d.pop("stroke_opacity", UNSET))

        def _parse_stroke_width(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        stroke_width = _parse_stroke_width(d.pop("stroke_width", UNSET))

        def _parse_fill_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fill_color = _parse_fill_color(d.pop("fill_color", UNSET))

        def _parse_fill_opacity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        fill_opacity = _parse_fill_opacity(d.pop("fill_opacity", UNSET))

        domain_style = cls(
            stroke_color=stroke_color,
            stroke_opacity=stroke_opacity,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )

        domain_style.additional_properties = d
        return domain_style

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
