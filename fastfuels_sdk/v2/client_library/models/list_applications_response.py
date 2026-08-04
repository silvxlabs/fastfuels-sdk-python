from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.application import Application


T = TypeVar("T", bound="ListApplicationsResponse")


@_attrs_define
class ListApplicationsResponse:
    """Paginated response for listing applications.

    Attributes:
        current_page (int): The current page number (zero-indexed).
        page_size (int): The number of items per page.
        total_items (int): The total number of items across all pages.
        applications (list[Application]): A list of applications.
    """

    current_page: int
    page_size: int
    total_items: int
    applications: list[Application]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_page = self.current_page

        page_size = self.page_size

        total_items = self.total_items

        applications = []
        for applications_item_data in self.applications:
            applications_item = applications_item_data.to_dict()
            applications.append(applications_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_page": current_page,
                "page_size": page_size,
                "total_items": total_items,
                "applications": applications,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.application import Application

        d = dict(src_dict)
        current_page = d.pop("current_page")

        page_size = d.pop("page_size")

        total_items = d.pop("total_items")

        applications = []
        _applications = d.pop("applications")
        for applications_item_data in _applications:
            applications_item = Application.from_dict(applications_item_data)

            applications.append(applications_item)

        list_applications_response = cls(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items,
            applications=applications,
        )

        list_applications_response.additional_properties = d
        return list_applications_response

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
