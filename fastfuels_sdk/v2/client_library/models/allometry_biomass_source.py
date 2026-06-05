from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

from ..models.biomass_component import BiomassComponent
from ..models.biomass_equations import BiomassEquations
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allometry_biomass_source_component_states import (
        AllometryBiomassSourceComponentStates,
    )
    from ..models.fine_biomass_config import FineBiomassConfig


T = TypeVar("T", bound="AllometryBiomassSource")


@_attrs_define
class AllometryBiomassSource:
    """Estimate biomass from allometric equations.

    Attributes:
        type_ (Literal['allometry'] | Unset):  Default: 'allometry'.
        equations (BiomassEquations | Unset): Allometric equation families for estimating biomass components.
        components (list[BiomassComponent] | Unset):
        component_states (AllometryBiomassSourceComponentStates | Unset): Per-component live/dead biomass partition
            fractions.
        fine (FineBiomassConfig | None | Unset):
    """

    type_: Literal["allometry"] | Unset = "allometry"
    equations: BiomassEquations | Unset = UNSET
    components: list[BiomassComponent] | Unset = UNSET
    component_states: AllometryBiomassSourceComponentStates | Unset = UNSET
    fine: FineBiomassConfig | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.fine_biomass_config import FineBiomassConfig

        type_ = self.type_

        equations: str | Unset = UNSET
        if not isinstance(self.equations, Unset):
            equations = self.equations.value

        components: list[str] | Unset = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.value
                components.append(components_item)

        component_states: dict[str, Any] | Unset = UNSET
        if not isinstance(self.component_states, Unset):
            component_states = self.component_states.to_dict()

        fine: dict[str, Any] | None | Unset
        if isinstance(self.fine, Unset):
            fine = UNSET
        elif isinstance(self.fine, FineBiomassConfig):
            fine = self.fine.to_dict()
        else:
            fine = self.fine

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if equations is not UNSET:
            field_dict["equations"] = equations
        if components is not UNSET:
            field_dict["components"] = components
        if component_states is not UNSET:
            field_dict["component_states"] = component_states
        if fine is not UNSET:
            field_dict["fine"] = fine

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allometry_biomass_source_component_states import (
            AllometryBiomassSourceComponentStates,
        )
        from ..models.fine_biomass_config import FineBiomassConfig

        d = dict(src_dict)
        type_ = cast(Literal["allometry"] | Unset, d.pop("type", UNSET))
        if type_ != "allometry" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'allometry', got '{type_}'")

        _equations = d.pop("equations", UNSET)
        equations: BiomassEquations | Unset
        if isinstance(_equations, Unset):
            equations = UNSET
        else:
            equations = BiomassEquations(_equations)

        _components = d.pop("components", UNSET)
        components: list[BiomassComponent] | Unset = UNSET
        if _components is not UNSET:
            components = []
            for components_item_data in _components:
                components_item = BiomassComponent(components_item_data)

                components.append(components_item)

        _component_states = d.pop("component_states", UNSET)
        component_states: AllometryBiomassSourceComponentStates | Unset
        if isinstance(_component_states, Unset):
            component_states = UNSET
        else:
            component_states = AllometryBiomassSourceComponentStates.from_dict(
                _component_states
            )

        def _parse_fine(data: object) -> FineBiomassConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fine_type_0 = FineBiomassConfig.from_dict(data)

                return fine_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FineBiomassConfig | None | Unset, data)

        fine = _parse_fine(d.pop("fine", UNSET))

        allometry_biomass_source = cls(
            type_=type_,
            equations=equations,
            components=components,
            component_states=component_states,
            fine=fine,
        )

        return allometry_biomass_source
