from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fia_species_group_share import FIASpeciesGroupShare


T = TypeVar("T", bound="TreeForestryMetrics")


@_attrs_define
class TreeForestryMetrics:
    """Stand-level forestry scalars for a tree inventory.

    Attributes:
        type_ (Literal['tree']):
        tree_count (int): Total trees in the inventory.
        basal_area_per_area (float | None): Stand basal area divided by domain area. Unit: ft**2/acre.
        tree_density (float | None): Trees per unit domain area (TPA). Unit: 1/acre.
        quadratic_mean_diameter (float | None): Quadratic mean DBH. Unit: in.
        dominant_species_groups (list[FIASpeciesGroupShare] | Unset): The N FIA species groups with the largest basal
            area share, sorted descending (N defaults to 5). Only the top N are returned; any remaining groups are omitted,
            so the listed shares may sum to less than 1.
    """

    type_: Literal["tree"]
    tree_count: int
    basal_area_per_area: float | None
    tree_density: float | None
    quadratic_mean_diameter: float | None
    dominant_species_groups: list[FIASpeciesGroupShare] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        tree_count = self.tree_count

        basal_area_per_area: float | None
        basal_area_per_area = self.basal_area_per_area

        tree_density: float | None
        tree_density = self.tree_density

        quadratic_mean_diameter: float | None
        quadratic_mean_diameter = self.quadratic_mean_diameter

        dominant_species_groups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.dominant_species_groups, Unset):
            dominant_species_groups = []
            for dominant_species_groups_item_data in self.dominant_species_groups:
                dominant_species_groups_item = (
                    dominant_species_groups_item_data.to_dict()
                )
                dominant_species_groups.append(dominant_species_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "tree_count": tree_count,
                "basal_area_per_area": basal_area_per_area,
                "tree_density": tree_density,
                "quadratic_mean_diameter": quadratic_mean_diameter,
            }
        )
        if dominant_species_groups is not UNSET:
            field_dict["dominant_species_groups"] = dominant_species_groups

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.fia_species_group_share import FIASpeciesGroupShare

        d = dict(src_dict)
        type_ = cast(Literal["tree"], d.pop("type"))
        if type_ != "tree":
            raise ValueError(f"type must match const 'tree', got '{type_}'")

        tree_count = d.pop("tree_count")

        def _parse_basal_area_per_area(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        basal_area_per_area = _parse_basal_area_per_area(d.pop("basal_area_per_area"))

        def _parse_tree_density(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        tree_density = _parse_tree_density(d.pop("tree_density"))

        def _parse_quadratic_mean_diameter(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        quadratic_mean_diameter = _parse_quadratic_mean_diameter(
            d.pop("quadratic_mean_diameter")
        )

        _dominant_species_groups = d.pop("dominant_species_groups", UNSET)
        dominant_species_groups: list[FIASpeciesGroupShare] | Unset = UNSET
        if _dominant_species_groups is not UNSET:
            dominant_species_groups = []
            for dominant_species_groups_item_data in _dominant_species_groups:
                dominant_species_groups_item = FIASpeciesGroupShare.from_dict(
                    dominant_species_groups_item_data
                )

                dominant_species_groups.append(dominant_species_groups_item)

        tree_forestry_metrics = cls(
            type_=type_,
            tree_count=tree_count,
            basal_area_per_area=basal_area_per_area,
            tree_density=tree_density,
            quadratic_mean_diameter=quadratic_mean_diameter,
            dominant_species_groups=dominant_species_groups,
        )

        tree_forestry_metrics.additional_properties = d
        return tree_forestry_metrics

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
