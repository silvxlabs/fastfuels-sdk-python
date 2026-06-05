from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory_expression_condition import InventoryExpressionCondition
    from ..models.inventory_feature_spatial_condition import (
        InventoryFeatureSpatialCondition,
    )
    from ..models.inventory_geometry_spatial_condition import (
        InventoryGeometrySpatialCondition,
    )
    from ..models.inventory_modification_action import InventoryModificationAction
    from ..models.inventory_modification_condition import InventoryModificationCondition
    from ..models.remove_action import RemoveAction


T = TypeVar("T", bound="InventoryModification")


@_attrs_define
class InventoryModification:
    """A modification rule: when all conditions match, apply actions.

    If a RemoveAction is present, it must be the only action.

        Attributes:
            conditions (list[InventoryExpressionCondition | InventoryFeatureSpatialCondition |
                InventoryGeometrySpatialCondition | InventoryModificationCondition]):
            actions (list[InventoryModificationAction | RemoveAction]):
    """

    conditions: list[
        InventoryExpressionCondition
        | InventoryFeatureSpatialCondition
        | InventoryGeometrySpatialCondition
        | InventoryModificationCondition
    ]
    actions: list[InventoryModificationAction | RemoveAction]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_expression_condition import InventoryExpressionCondition
        from ..models.inventory_geometry_spatial_condition import (
            InventoryGeometrySpatialCondition,
        )
        from ..models.inventory_modification_action import InventoryModificationAction
        from ..models.inventory_modification_condition import (
            InventoryModificationCondition,
        )

        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item: dict[str, Any]
            if isinstance(conditions_item_data, InventoryModificationCondition):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, InventoryExpressionCondition):
                conditions_item = conditions_item_data.to_dict()
            elif isinstance(conditions_item_data, InventoryGeometrySpatialCondition):
                conditions_item = conditions_item_data.to_dict()
            else:
                conditions_item = conditions_item_data.to_dict()

            conditions.append(conditions_item)

        actions = []
        for actions_item_data in self.actions:
            actions_item: dict[str, Any]
            if isinstance(actions_item_data, InventoryModificationAction):
                actions_item = actions_item_data.to_dict()
            else:
                actions_item = actions_item_data.to_dict()

            actions.append(actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conditions": conditions,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory_expression_condition import InventoryExpressionCondition
        from ..models.inventory_feature_spatial_condition import (
            InventoryFeatureSpatialCondition,
        )
        from ..models.inventory_geometry_spatial_condition import (
            InventoryGeometrySpatialCondition,
        )
        from ..models.inventory_modification_action import InventoryModificationAction
        from ..models.inventory_modification_condition import (
            InventoryModificationCondition,
        )
        from ..models.remove_action import RemoveAction

        d = dict(src_dict)
        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:

            def _parse_conditions_item(
                data: object,
            ) -> (
                InventoryExpressionCondition
                | InventoryFeatureSpatialCondition
                | InventoryGeometrySpatialCondition
                | InventoryModificationCondition
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_0 = InventoryModificationCondition.from_dict(
                        data
                    )

                    return conditions_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_1 = InventoryExpressionCondition.from_dict(
                        data
                    )

                    return conditions_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_2_type_0 = (
                        InventoryGeometrySpatialCondition.from_dict(data)
                    )

                    return conditions_item_type_2_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                conditions_item_type_2_type_1 = (
                    InventoryFeatureSpatialCondition.from_dict(data)
                )

                return conditions_item_type_2_type_1

            conditions_item = _parse_conditions_item(conditions_item_data)

            conditions.append(conditions_item)

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:

            def _parse_actions_item(
                data: object,
            ) -> InventoryModificationAction | RemoveAction:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_0 = InventoryModificationAction.from_dict(data)

                    return actions_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                actions_item_type_1 = RemoveAction.from_dict(data)

                return actions_item_type_1

            actions_item = _parse_actions_item(actions_item_data)

            actions.append(actions_item)

        inventory_modification = cls(
            conditions=conditions,
            actions=actions,
        )

        inventory_modification.additional_properties = d
        return inventory_modification

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
