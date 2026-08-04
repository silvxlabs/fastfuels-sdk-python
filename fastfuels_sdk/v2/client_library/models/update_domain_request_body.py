from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.domain_style import DomainStyle


T = TypeVar("T", bound="UpdateDomainRequestBody")


@_attrs_define
class UpdateDomainRequestBody:
    """Request body for updating a domain's metadata.

    All fields are optional. Only provided fields will be updated.
    Geometry (features) and CRS cannot be modified after creation.

        Attributes:
            name (None | str | Unset): The name of the domain.
            description (None | str | Unset): A description of the domain.
            tags (list[str] | None | Unset): A list of tags associated with the domain.
            style (DomainStyle | None | Unset): Update visual style fields. Only provided sub-fields are merged into the
                existing style; unspecified sub-fields preserve their current values.
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    style: DomainStyle | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.domain_style import DomainStyle

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        style: dict[str, Any] | None | Unset
        if isinstance(self.style, Unset):
            style = UNSET
        elif isinstance(self.style, DomainStyle):
            style = self.style.to_dict()
        else:
            style = self.style

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.domain_style import DomainStyle

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_style(data: object) -> DomainStyle | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                style_type_0 = DomainStyle.from_dict(data)

                return style_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DomainStyle | None | Unset, data)

        style = _parse_style(d.pop("style", UNSET))

        update_domain_request_body = cls(
            name=name,
            description=description,
            tags=tags,
            style=style,
        )

        update_domain_request_body.additional_properties = d
        return update_domain_request_body

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
