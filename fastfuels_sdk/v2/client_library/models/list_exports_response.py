from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.export import Export


T = TypeVar("T", bound="ListExportsResponse")


@_attrs_define
class ListExportsResponse:
    """Paginated response for listing exports.

    Attributes:
        current_page (int): The current page number (zero-indexed).
        page_size (int): The number of items per page.
        total_items (int): The total number of items across all pages.
        exports (list[Export]):
    """

    current_page: int
    page_size: int
    total_items: int
    exports: list[Export]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_page = self.current_page

        page_size = self.page_size

        total_items = self.total_items

        exports = []
        for exports_item_data in self.exports:
            exports_item = exports_item_data.to_dict()
            exports.append(exports_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_page": current_page,
                "page_size": page_size,
                "total_items": total_items,
                "exports": exports,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export import Export

        d = dict(src_dict)
        current_page = d.pop("current_page")

        page_size = d.pop("page_size")

        total_items = d.pop("total_items")

        exports = []
        _exports = d.pop("exports")
        for exports_item_data in _exports:
            exports_item = Export.from_dict(exports_item_data)

            exports.append(exports_item)

        list_exports_response = cls(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            exports=exports,
        )

        list_exports_response.additional_properties = d
        return list_exports_response

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
