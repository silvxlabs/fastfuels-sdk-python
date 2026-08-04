from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.grid import Grid


T = TypeVar("T", bound="ListGridsResponse")


@_attrs_define
class ListGridsResponse:
    """Paginated response for listing grids.

    Attributes:
        current_page (int): The current page number (zero-indexed).
        page_size (int): The number of items per page.
        total_items (int): The total number of items across all pages.
        grids (list[Grid]):
    """

    current_page: int
    page_size: int
    total_items: int
    grids: list[Grid]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_page = self.current_page

        page_size = self.page_size

        total_items = self.total_items

        grids = []
        for grids_item_data in self.grids:
            grids_item = grids_item_data.to_dict()
            grids.append(grids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_page": current_page,
                "page_size": page_size,
                "total_items": total_items,
                "grids": grids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.grid import Grid

        d = dict(src_dict)
        current_page = d.pop("current_page")

        page_size = d.pop("page_size")

        total_items = d.pop("total_items")

        grids = []
        _grids = d.pop("grids")
        for grids_item_data in _grids:
            grids_item = Grid.from_dict(grids_item_data)

            grids.append(grids_item)

        list_grids_response = cls(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            grids=grids,
        )

        list_grids_response.additional_properties = d
        return list_grids_response

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
