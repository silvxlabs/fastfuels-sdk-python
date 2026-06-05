from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.domain import Domain


T = TypeVar("T", bound="ListDomainsResponse")


@_attrs_define
class ListDomainsResponse:
    """Paginated response for listing domain resources.

    Attributes:
        current_page (int): The current page number (zero-indexed).
        page_size (int): The number of items per page.
        total_items (int): The total number of items across all pages.
        domains (list[Domain]): The list of domain resources for the current page.
    """

    current_page: int
    page_size: int
    total_items: int
    domains: list[Domain]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_page = self.current_page

        page_size = self.page_size

        total_items = self.total_items

        domains = []
        for domains_item_data in self.domains:
            domains_item = domains_item_data.to_dict()
            domains.append(domains_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_page": current_page,
                "page_size": page_size,
                "total_items": total_items,
                "domains": domains,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.domain import Domain

        d = dict(src_dict)
        current_page = d.pop("current_page")

        page_size = d.pop("page_size")

        total_items = d.pop("total_items")

        domains = []
        _domains = d.pop("domains")
        for domains_item_data in _domains:
            domains_item = Domain.from_dict(domains_item_data)

            domains.append(domains_item)

        list_domains_response = cls(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            domains=domains,
        )

        list_domains_response.additional_properties = d
        return list_domains_response

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
