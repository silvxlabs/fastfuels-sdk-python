from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportGridRequest")


@_attrs_define
class ExportGridRequest:
    """Request body for creating a grid export.

    Used at: POST /domains/{domain_id}/grids/{grid_id}/exports/{format}

        Attributes:
            bands (list[str] | None | Unset): Band keys to include (e.g. 'fuel_load.1hr', 'fbfm'). Omit to export all bands
                from the grid.
            expiration_days (int | Unset): Number of days until the signed download URL expires (max 7). Default: 7.
                Default: 7.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
    """

    bands: list[str] | None | Unset = UNSET
    expiration_days: int | Unset = 7
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bands: list[str] | None | Unset
        if isinstance(self.bands, Unset):
            bands = UNSET
        elif isinstance(self.bands, list):
            bands = self.bands

        else:
            bands = self.bands

        expiration_days = self.expiration_days

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bands is not UNSET:
            field_dict["bands"] = bands
        if expiration_days is not UNSET:
            field_dict["expiration_days"] = expiration_days
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

        def _parse_bands(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                bands_type_0 = cast(list[str], data)

                return bands_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        bands = _parse_bands(d.pop("bands", UNSET))

        expiration_days = d.pop("expiration_days", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        export_grid_request = cls(
            bands=bands,
            expiration_days=expiration_days,
            name=name,
            description=description,
            tags=tags,
        )

        export_grid_request.additional_properties = d
        return export_grid_request

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
