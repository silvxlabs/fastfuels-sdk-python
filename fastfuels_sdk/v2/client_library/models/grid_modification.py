from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.grid_feature_spatial_condition import GridFeatureSpatialCondition
    from ..models.grid_geometry_spatial_condition import GridGeometrySpatialCondition
    from ..models.grid_modification_action import GridModificationAction
    from ..models.grid_modification_condition import GridModificationCondition


T = TypeVar("T", bound="GridModification")


@_attrs_define
class GridModification:
    """A grid modification rule: a list of conditions and a list of actions.

    Conditions can be band-based (checking values) or spatial (checking
    location). All conditions in a rule are **ANDed** — the actions apply only
    to cells that satisfy *every* condition, so adding a condition narrows the
    selection (the intersection).

    There is no OR within a rule. To act on a **union** of selections (e.g.
    roads *or* water bodies), supply multiple rules: each rule is applied
    independently, so adding a rule widens the overall selection. Putting two
    mutually exclusive conditions (a road feature AND a water feature) in one
    rule selects cells that are both at once — usually none.

    An **empty `conditions` list applies the actions to the whole grid** —
    every cell. Use it for a blanket adjustment (e.g. subtract a constant from
    every cell); add conditions to narrow it to a region or value range.

        Attributes:
            actions (list[GridModificationAction]): Actions to apply when conditions match
            conditions (list[GridFeatureSpatialCondition | GridGeometrySpatialCondition | GridModificationCondition] |
                Unset): Conditions that must all be true (ANDed). An empty list applies the actions to the whole grid — every
                cell.
    """

    actions: list[GridModificationAction]
    conditions: (
        list[
            GridFeatureSpatialCondition
            | GridGeometrySpatialCondition
            | GridModificationCondition
        ]
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.grid_geometry_spatial_condition import (
            GridGeometrySpatialCondition,
        )
        from ..models.grid_modification_condition import GridModificationCondition

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        conditions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                conditions_item: dict[str, Any]
                if isinstance(
                    conditions_item_data, GridModificationCondition
                ) or isinstance(conditions_item_data, GridGeometrySpatialCondition):
                    conditions_item = conditions_item_data.to_dict()
                else:
                    conditions_item = conditions_item_data.to_dict()

                conditions.append(conditions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actions": actions,
            }
        )
        if conditions is not UNSET:
            field_dict["conditions"] = conditions

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.grid_feature_spatial_condition import GridFeatureSpatialCondition
        from ..models.grid_geometry_spatial_condition import (
            GridGeometrySpatialCondition,
        )
        from ..models.grid_modification_action import GridModificationAction
        from ..models.grid_modification_condition import GridModificationCondition

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = GridModificationAction.from_dict(actions_item_data)

            actions.append(actions_item)

        _conditions = d.pop("conditions", UNSET)
        conditions: (
            list[
                GridFeatureSpatialCondition
                | GridGeometrySpatialCondition
                | GridModificationCondition
            ]
            | Unset
        ) = UNSET
        if _conditions is not UNSET:
            conditions = []
            for conditions_item_data in _conditions:

                def _parse_conditions_item(
                    data: object,
                ) -> (
                    GridFeatureSpatialCondition
                    | GridGeometrySpatialCondition
                    | GridModificationCondition
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        conditions_item_type_0 = GridModificationCondition.from_dict(
                            data
                        )

                        return conditions_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        conditions_item_type_1_type_0 = (
                            GridGeometrySpatialCondition.from_dict(data)
                        )

                        return conditions_item_type_1_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_1_type_1 = (
                        GridFeatureSpatialCondition.from_dict(data)
                    )

                    return conditions_item_type_1_type_1

                conditions_item = _parse_conditions_item(conditions_item_data)

                conditions.append(conditions_item)

        grid_modification = cls(
            actions=actions,
            conditions=conditions,
        )

        grid_modification.additional_properties = d
        return grid_modification

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
