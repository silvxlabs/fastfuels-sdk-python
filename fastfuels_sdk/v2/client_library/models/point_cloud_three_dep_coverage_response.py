from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.three_dep_dataset_coverage import ThreeDepDatasetCoverage


T = TypeVar("T", bound="PointCloudThreeDepCoverageResponse")


@_attrs_define
class PointCloudThreeDepCoverageResponse:
    """Response model for the 3DEP point cloud coverage pre-flight check.

    Attributes:
        available (bool): Whether any 3DEP lidar covers this domain. When false, a create request for this domain is
            rejected.
        coverage_fraction (float): Fraction of the domain covered by 3DEP lidar, from `0.0` to `1.0`. This is the union
            of every available acquisition, so it never exceeds 1.0 no matter how much the acquisitions overlap.
        datasets (list[ThreeDepDatasetCoverage]): Acquisitions that would be read, in the order they would be used.
            Empty when no lidar covers the domain.
        estimated_point_count (int): Approximate total number of points a fetch would return, summed across
            acquisitions.
        point_budget (int): Maximum number of points a single fetch may return. Shrink the domain if the estimate
            exceeds it.
        exceeds_point_budget (bool): Whether the estimate is over `point_budget`. When true, a create request for this
            domain is rejected, so check this before committing to a fetch.
    """

    available: bool
    coverage_fraction: float
    datasets: list[ThreeDepDatasetCoverage]
    estimated_point_count: int
    point_budget: int
    exceeds_point_budget: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        coverage_fraction = self.coverage_fraction

        datasets = []
        for datasets_item_data in self.datasets:
            datasets_item = datasets_item_data.to_dict()
            datasets.append(datasets_item)

        estimated_point_count = self.estimated_point_count

        point_budget = self.point_budget

        exceeds_point_budget = self.exceeds_point_budget

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
                "coverage_fraction": coverage_fraction,
                "datasets": datasets,
                "estimated_point_count": estimated_point_count,
                "point_budget": point_budget,
                "exceeds_point_budget": exceeds_point_budget,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.three_dep_dataset_coverage import ThreeDepDatasetCoverage

        d = dict(src_dict)
        available = d.pop("available")

        coverage_fraction = d.pop("coverage_fraction")

        datasets = []
        _datasets = d.pop("datasets")
        for datasets_item_data in _datasets:
            datasets_item = ThreeDepDatasetCoverage.from_dict(datasets_item_data)

            datasets.append(datasets_item)

        estimated_point_count = d.pop("estimated_point_count")

        point_budget = d.pop("point_budget")

        exceeds_point_budget = d.pop("exceeds_point_budget")

        point_cloud_three_dep_coverage_response = cls(
            available=available,
            coverage_fraction=coverage_fraction,
            datasets=datasets,
            estimated_point_count=estimated_point_count,
            point_budget=point_budget,
            exceeds_point_budget=exceeds_point_budget,
        )

        point_cloud_three_dep_coverage_response.additional_properties = d
        return point_cloud_three_dep_coverage_response

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
