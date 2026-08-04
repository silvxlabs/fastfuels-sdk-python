from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.grid_data_response_order import GridDataResponseOrder

if TYPE_CHECKING:
    from ..models.dense_grid_data import DenseGridData
    from ..models.grid_data_chunk_metadata import GridDataChunkMetadata
    from ..models.sparse_grid_data import SparseGridData


T = TypeVar("T", bound="GridDataResponse")


@_attrs_define
class GridDataResponse:
    """
    Attributes:
        shape (list[int]):
        order (GridDataResponseOrder):
        metadata (GridDataChunkMetadata):
        data (DenseGridData | SparseGridData):
    """

    shape: list[int]
    order: GridDataResponseOrder
    metadata: GridDataChunkMetadata
    data: DenseGridData | SparseGridData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dense_grid_data import DenseGridData

        shape = self.shape

        order = self.order.value

        metadata = self.metadata.to_dict()

        data: dict[str, Any]
        if isinstance(self.data, DenseGridData):
            data = self.data.to_dict()
        else:
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shape": shape,
                "order": order,
                "metadata": metadata,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.dense_grid_data import DenseGridData
        from ..models.grid_data_chunk_metadata import GridDataChunkMetadata
        from ..models.sparse_grid_data import SparseGridData

        d = dict(src_dict)
        shape = cast(list[int], d.pop("shape"))

        order = GridDataResponseOrder(d.pop("order"))

        metadata = GridDataChunkMetadata.from_dict(d.pop("metadata"))

        def _parse_data(data: object) -> DenseGridData | SparseGridData:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = DenseGridData.from_dict(data)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            data_type_1 = SparseGridData.from_dict(data)

            return data_type_1

        data = _parse_data(d.pop("data"))

        grid_data_response = cls(
            shape=shape,
            order=order,
            metadata=metadata,
            data=data,
        )

        grid_data_response.additional_properties = d
        return grid_data_response

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
