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
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fine_biomass_config import FineBiomassConfig
    from ..models.inventory_columns_biomass_source_columns import (
        InventoryColumnsBiomassSourceColumns,
    )
    from ..models.inventory_columns_biomass_source_component_states import (
        InventoryColumnsBiomassSourceComponentStates,
    )


T = TypeVar("T", bound="InventoryColumnsBiomassSource")


@_attrs_define
class InventoryColumnsBiomassSource:
    """Read per-tree component biomass from inventory columns.

    Attributes:
        columns (InventoryColumnsBiomassSourceColumns): Per-component inventory columns. Values must be per-tree kg.
        type_ (Literal['inventory_columns'] | Unset):  Default: 'inventory_columns'.
        components (list[BiomassComponent] | Unset):
        component_states (InventoryColumnsBiomassSourceComponentStates | Unset): Per-component live/dead biomass
            partition fractions.
        fine (FineBiomassConfig | None | Unset):
    """

    columns: InventoryColumnsBiomassSourceColumns
    type_: Literal["inventory_columns"] | Unset = "inventory_columns"
    components: list[BiomassComponent] | Unset = UNSET
    component_states: InventoryColumnsBiomassSourceComponentStates | Unset = UNSET
    fine: FineBiomassConfig | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.fine_biomass_config import FineBiomassConfig

        columns = self.columns.to_dict()

        type_ = self.type_

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

        field_dict.update(
            {
                "columns": columns,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if components is not UNSET:
            field_dict["components"] = components
        if component_states is not UNSET:
            field_dict["component_states"] = component_states
        if fine is not UNSET:
            field_dict["fine"] = fine

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fine_biomass_config import FineBiomassConfig
        from ..models.inventory_columns_biomass_source_columns import (
            InventoryColumnsBiomassSourceColumns,
        )
        from ..models.inventory_columns_biomass_source_component_states import (
            InventoryColumnsBiomassSourceComponentStates,
        )

        d = dict(src_dict)
        columns = InventoryColumnsBiomassSourceColumns.from_dict(d.pop("columns"))

        type_ = cast(Literal["inventory_columns"] | Unset, d.pop("type", UNSET))
        if type_ != "inventory_columns" and not isinstance(type_, Unset):
            raise ValueError(
                f"type must match const 'inventory_columns', got '{type_}'"
            )

        _components = d.pop("components", UNSET)
        components: list[BiomassComponent] | Unset = UNSET
        if _components is not UNSET:
            components = []
            for components_item_data in _components:
                components_item = BiomassComponent(components_item_data)

                components.append(components_item)

        _component_states = d.pop("component_states", UNSET)
        component_states: InventoryColumnsBiomassSourceComponentStates | Unset
        if isinstance(_component_states, Unset):
            component_states = UNSET
        else:
            component_states = InventoryColumnsBiomassSourceComponentStates.from_dict(
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

        inventory_columns_biomass_source = cls(
            columns=columns,
            type_=type_,
            components=components,
            component_states=component_states,
            fine=fine,
        )

        return inventory_columns_biomass_source
