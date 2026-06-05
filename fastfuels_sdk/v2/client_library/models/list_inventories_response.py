from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory import Inventory


T = TypeVar("T", bound="ListInventoriesResponse")


@_attrs_define
class ListInventoriesResponse:
    """Paginated response for listing inventories.

    Attributes:
        current_page (int): The current page number (zero-indexed).
        page_size (int): The number of items per page.
        total_items (int): The total number of items across all pages.
        inventories (list[Inventory]):
    """

    current_page: int
    page_size: int
    total_items: int
    inventories: list[Inventory]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_page = self.current_page

        page_size = self.page_size

        total_items = self.total_items

        inventories = []
        for inventories_item_data in self.inventories:
            inventories_item = inventories_item_data.to_dict()
            inventories.append(inventories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_page": current_page,
                "page_size": page_size,
                "total_items": total_items,
                "inventories": inventories,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory import Inventory

        d = dict(src_dict)
        current_page = d.pop("current_page")

        page_size = d.pop("page_size")

        total_items = d.pop("total_items")

        inventories = []
        _inventories = d.pop("inventories")
        for inventories_item_data in _inventories:
            inventories_item = Inventory.from_dict(inventories_item_data)

            inventories.append(inventories_item)

        list_inventories_response = cls(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            inventories=inventories,
        )

        list_inventories_response.additional_properties = d
        return list_inventories_response

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
