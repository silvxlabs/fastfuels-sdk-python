from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.biomass_component_state import BiomassComponentState


T = TypeVar("T", bound="AllometryBiomassSourceComponentStates")


@_attrs_define
class AllometryBiomassSourceComponentStates:
    """Per-component live/dead biomass partition fractions."""

    additional_properties: dict[str, BiomassComponentState] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.biomass_component_state import BiomassComponentState

        d = dict(src_dict)
        allometry_biomass_source_component_states = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = BiomassComponentState.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        allometry_biomass_source_component_states.additional_properties = (
            additional_properties
        )
        return allometry_biomass_source_component_states

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> BiomassComponentState:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: BiomassComponentState) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
