from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory_data_response_data_type_1_item import (
        InventoryDataResponseDataType1Item,
    )


T = TypeVar("T", bound="InventoryDataResponse")


@_attrs_define
class InventoryDataResponse:
    """
    Attributes:
        partition (int):
        num_rows (int):
        columns (list[str]):
        data (list[InventoryDataResponseDataType1Item] | list[list[Any]]):
    """

    partition: int
    num_rows: int
    columns: list[str]
    data: list[InventoryDataResponseDataType1Item] | list[list[Any]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        partition = self.partition

        num_rows = self.num_rows

        columns = self.columns

        data: list[dict[str, Any]] | list[list[Any]]
        if isinstance(self.data, list):
            data = []
            for data_type_0_item_data in self.data:
                data_type_0_item = data_type_0_item_data

                data.append(data_type_0_item)

        else:
            data = []
            for data_type_1_item_data in self.data:
                data_type_1_item = data_type_1_item_data.to_dict()
                data.append(data_type_1_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partition": partition,
                "num_rows": num_rows,
                "columns": columns,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory_data_response_data_type_1_item import (
            InventoryDataResponseDataType1Item,
        )

        d = dict(src_dict)
        partition = d.pop("partition")

        num_rows = d.pop("num_rows")

        columns = cast(list[str], d.pop("columns"))

        def _parse_data(
            data: object,
        ) -> list[InventoryDataResponseDataType1Item] | list[list[Any]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_type_0 = []
                _data_type_0 = data
                for data_type_0_item_data in _data_type_0:
                    data_type_0_item = cast(list[Any], data_type_0_item_data)

                    data_type_0.append(data_type_0_item)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, list):
                raise TypeError()
            data_type_1 = []
            _data_type_1 = data
            for data_type_1_item_data in _data_type_1:
                data_type_1_item = InventoryDataResponseDataType1Item.from_dict(
                    data_type_1_item_data
                )

                data_type_1.append(data_type_1_item)

            return data_type_1

        data = _parse_data(d.pop("data"))

        inventory_data_response = cls(
            partition=partition,
            num_rows=num_rows,
            columns=columns,
            data=data,
        )

        inventory_data_response.additional_properties = d
        return inventory_data_response

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
