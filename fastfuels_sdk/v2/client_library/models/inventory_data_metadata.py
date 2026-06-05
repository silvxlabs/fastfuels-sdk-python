from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory_partition_info import InventoryPartitionInfo


T = TypeVar("T", bound="InventoryDataMetadata")


@_attrs_define
class InventoryDataMetadata:
    """
    Attributes:
        inventory_id (str):
        num_partitions (int):
        total_rows (int):
        columns (list[str]):
        partitions (list[InventoryPartitionInfo]):
    """

    inventory_id: str
    num_partitions: int
    total_rows: int
    columns: list[str]
    partitions: list[InventoryPartitionInfo]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inventory_id = self.inventory_id

        num_partitions = self.num_partitions

        total_rows = self.total_rows

        columns = self.columns

        partitions = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inventory_id": inventory_id,
                "num_partitions": num_partitions,
                "total_rows": total_rows,
                "columns": columns,
                "partitions": partitions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory_partition_info import InventoryPartitionInfo

        d = dict(src_dict)
        inventory_id = d.pop("inventory_id")

        num_partitions = d.pop("num_partitions")

        total_rows = d.pop("total_rows")

        columns = cast(list[str], d.pop("columns"))

        partitions = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = InventoryPartitionInfo.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        inventory_data_metadata = cls(
            inventory_id=inventory_id,
            num_partitions=num_partitions,
            total_rows=total_rows,
            columns=columns,
            partitions=partitions,
        )

        inventory_data_metadata.additional_properties = d
        return inventory_data_metadata

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
