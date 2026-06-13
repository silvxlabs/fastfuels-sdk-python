from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_gdam_inventory_request_impute_columns_item import (
    CreateGdamInventoryRequestImputeColumnsItem,
)
from ..models.inventory_type import InventoryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateGdamInventoryRequest")


@_attrs_define
class CreateGdamInventoryRequest:
    """Request body for creating an inventory via GDAM allometry imputation.

    Attributes:
        source_tree_inventory_id (str): ID of a completed tree inventory whose missing morphology columns (dbh, crown
            ratio, species) GDAM will fill in. Existing values are preserved; only missing cells are imputed.
        type_ (InventoryType | Unset): Type of entities in the inventory.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        impute_columns (list[CreateGdamInventoryRequestImputeColumnsItem] | Unset): Which morphology columns GDAM should
            impute. Defaults to all of `dbh`, `crown_ratio`, `fia_species_code`. Narrow it (e.g. `['fia_species_code']`) to
            impute fewer columns and write less to disk; columns left out are not imputed (they stay as the source had
            them). Must contain at least one column, with no duplicates.
    """

    source_tree_inventory_id: str
    type_: InventoryType | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    impute_columns: list[CreateGdamInventoryRequestImputeColumnsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_tree_inventory_id = self.source_tree_inventory_id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        impute_columns: list[str] | Unset = UNSET
        if not isinstance(self.impute_columns, Unset):
            impute_columns = []
            for impute_columns_item_data in self.impute_columns:
                impute_columns_item = impute_columns_item_data.value
                impute_columns.append(impute_columns_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_tree_inventory_id": source_tree_inventory_id,
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
        if impute_columns is not UNSET:
            field_dict["impute_columns"] = impute_columns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_tree_inventory_id = d.pop("source_tree_inventory_id")

        _type_ = d.pop("type", UNSET)
        type_: InventoryType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = InventoryType(_type_)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _impute_columns = d.pop("impute_columns", UNSET)
        impute_columns: list[CreateGdamInventoryRequestImputeColumnsItem] | Unset = (
            UNSET
        )
        if _impute_columns is not UNSET:
            impute_columns = []
            for impute_columns_item_data in _impute_columns:
                impute_columns_item = CreateGdamInventoryRequestImputeColumnsItem(
                    impute_columns_item_data
                )

                impute_columns.append(impute_columns_item)

        create_gdam_inventory_request = cls(
            source_tree_inventory_id=source_tree_inventory_id,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            impute_columns=impute_columns,
        )

        create_gdam_inventory_request.additional_properties = d
        return create_gdam_inventory_request

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
