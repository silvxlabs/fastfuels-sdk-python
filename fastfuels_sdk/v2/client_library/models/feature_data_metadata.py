from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feature_partition_info import FeaturePartitionInfo


T = TypeVar("T", bound="FeatureDataMetadata")


@_attrs_define
class FeatureDataMetadata:
    """Partition layout for a feature blob.

    Attributes:
        total_features (int): Total number of features across all partitions.
        partition_count (int): Number of valid `partition_index` values. Iterate from 0 to `partition_count - 1` to
            retrieve every feature exactly once.
        partitions (list[FeaturePartitionInfo]): Per-partition row counts read from the GeoParquet footer. Useful for
            sizing client-side buffers.
    """

    total_features: int
    partition_count: int
    partitions: list[FeaturePartitionInfo]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_features = self.total_features

        partition_count = self.partition_count

        partitions = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_features": total_features,
                "partition_count": partition_count,
                "partitions": partitions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.feature_partition_info import FeaturePartitionInfo

        d = dict(src_dict)
        total_features = d.pop("total_features")

        partition_count = d.pop("partition_count")

        partitions = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = FeaturePartitionInfo.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        feature_data_metadata = cls(
            total_features=total_features,
            partition_count=partition_count,
            partitions=partitions,
        )

        feature_data_metadata.additional_properties = d
        return feature_data_metadata

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
