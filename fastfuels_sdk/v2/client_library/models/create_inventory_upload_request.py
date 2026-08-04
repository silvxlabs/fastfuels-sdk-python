from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inventory_upload_format import InventoryUploadFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inventory_column_mapping import InventoryColumnMapping


T = TypeVar("T", bound="CreateInventoryUploadRequest")


@_attrs_define
class CreateInventoryUploadRequest:
    """
    Attributes:
        format_ (InventoryUploadFormat):
        columns (InventoryColumnMapping | Unset): Maps v2 column names to the corresponding column names in the uploaded
            file.

            Omit any entry whose column already uses the v2 name. For GeoJSON and
            GeoPackage formats, x and y are extracted from geometry — their mapping
            entries are ignored.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
    """

    format_: InventoryUploadFormat
    columns: InventoryColumnMapping | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        format_ = self.format_.value

        columns: dict[str, Any] | Unset = UNSET
        if not isinstance(self.columns, Unset):
            columns = self.columns.to_dict()

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "format": format_,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory_column_mapping import InventoryColumnMapping

        d = dict(src_dict)
        format_ = InventoryUploadFormat(d.pop("format"))

        _columns = d.pop("columns", UNSET)
        columns: InventoryColumnMapping | Unset
        if isinstance(_columns, Unset):
            columns = UNSET
        else:
            columns = InventoryColumnMapping.from_dict(_columns)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        create_inventory_upload_request = cls(
            format_=format_,
            columns=columns,
            name=name,
            description=description,
            tags=tags,
        )

        create_inventory_upload_request.additional_properties = d
        return create_inventory_upload_request

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
