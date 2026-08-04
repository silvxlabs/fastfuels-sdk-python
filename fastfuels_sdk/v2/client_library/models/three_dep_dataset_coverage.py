from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ThreeDepDatasetCoverage")


@_attrs_define
class ThreeDepDatasetCoverage:
    """One 3DEP acquisition available over a domain, and what it would supply.

    Attributes:
        name (str): USGS acquisition name. Pass it in `datasets` on a create request to pin the fetch to this
            acquisition.
        url (str): Location of the acquisition's Entwine Point Tile index.
        contribution_fraction (float): Fraction of the domain this acquisition would supply, from `0.0` to `1.0`.
            Acquisitions overlap each other freely, so this is the share left over after the acquisitions listed before it
            have taken their part — not the raw overlap. The values are therefore disjoint and sum to `coverage_fraction`.
        estimated_density (float): Average point density of the acquisition, in points per square metre, computed over
            its full published extent.
        estimated_points (int): Approximate number of points this acquisition would contribute. Derived from its density
            and the area it covers, so treat it as an order-of-magnitude figure rather than an exact count.
    """

    name: str
    url: str
    contribution_fraction: float
    estimated_density: float
    estimated_points: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        url = self.url

        contribution_fraction = self.contribution_fraction

        estimated_density = self.estimated_density

        estimated_points = self.estimated_points

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "url": url,
                "contribution_fraction": contribution_fraction,
                "estimated_density": estimated_density,
                "estimated_points": estimated_points,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        url = d.pop("url")

        contribution_fraction = d.pop("contribution_fraction")

        estimated_density = d.pop("estimated_density")

        estimated_points = d.pop("estimated_points")

        three_dep_dataset_coverage = cls(
            name=name,
            url=url,
            contribution_fraction=contribution_fraction,
            estimated_density=estimated_density,
            estimated_points=estimated_points,
        )

        three_dep_dataset_coverage.additional_properties = d
        return three_dep_dataset_coverage

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
