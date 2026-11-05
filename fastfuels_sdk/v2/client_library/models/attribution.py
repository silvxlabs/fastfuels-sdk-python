from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Attribution")


@_attrs_define
class Attribution:
    """License and citation for one third-party dataset used by a resource.

    Attributes:
        dataset (str): Name of the source dataset.
        license_name (str): SPDX identifier of the dataset's license.
        license_url (str): Link to the full license text.
        citation (str): Attribution text to reproduce wherever the data is shown or shared.
        access_url (str): Where to find the dataset and its terms of use.
        accessed_on (str): Date the data was retrieved, as YYYY-MM-DD.
    """

    dataset: str
    license_name: str
    license_url: str
    citation: str
    access_url: str
    accessed_on: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset = self.dataset

        license_name = self.license_name

        license_url = self.license_url

        citation = self.citation

        access_url = self.access_url

        accessed_on = self.accessed_on

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset": dataset,
                "license_name": license_name,
                "license_url": license_url,
                "citation": citation,
                "access_url": access_url,
                "accessed_on": accessed_on,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        dataset = d.pop("dataset")

        license_name = d.pop("license_name")

        license_url = d.pop("license_url")

        citation = d.pop("citation")

        access_url = d.pop("access_url")

        accessed_on = d.pop("accessed_on")

        attribution = cls(
            dataset=dataset,
            license_name=license_name,
            license_url=license_url,
            citation=citation,
            access_url=access_url,
            accessed_on=accessed_on,
        )

        attribution.additional_properties = d
        return attribution

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
