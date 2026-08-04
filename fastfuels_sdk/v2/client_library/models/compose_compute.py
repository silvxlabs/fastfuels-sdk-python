from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.compose_operator import ComposeOperator
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compose_attribute_condition import ComposeAttributeCondition
    from ..models.compose_literal import ComposeLiteral
    from ..models.grid_feature_spatial_condition import GridFeatureSpatialCondition
    from ..models.grid_geometry_spatial_condition import GridGeometrySpatialCondition
    from ..models.inline_compute import InlineCompute


T = TypeVar("T", bound="ComposeCompute")


@_attrs_define
class ComposeCompute:
    """Compute an output band from one or more operands.

    The output band is always continuous and its unit is derived from the
    operands (the product/quotient for `multiply`/`divide`, the operand unit
    otherwise). Supply `unit` only to express the result in a different but
    dimensionally compatible unit; the worker converts to it.

        Attributes:
            operator (ComposeOperator): Operators available for compose computations.
            operands (list[ComposeLiteral | float | int | str]):
            output (str): Output band key, e.g. `fuel_load.1hr`.
            name (None | str | Unset): Optional display name for the output band.
            description (None | str | Unset): Optional description for the output band.
            unit (None | str | Unset): Optional canonical output unit. Defaults to the unit derived from the operands; if
                given it must be dimensionally compatible.
            conditions (list[ComposeAttributeCondition | GridFeatureSpatialCondition | GridGeometrySpatialCondition] | None
                | Unset):
            else_ (ComposeLiteral | float | InlineCompute | int | None | str | Unset):
    """

    operator: ComposeOperator
    operands: list[ComposeLiteral | float | int | str]
    output: str
    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    unit: None | str | Unset = UNSET
    conditions: (
        list[
            ComposeAttributeCondition
            | GridFeatureSpatialCondition
            | GridGeometrySpatialCondition
        ]
        | None
        | Unset
    ) = UNSET
    else_: ComposeLiteral | float | InlineCompute | int | None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.compose_attribute_condition import ComposeAttributeCondition
        from ..models.compose_literal import ComposeLiteral
        from ..models.grid_geometry_spatial_condition import (
            GridGeometrySpatialCondition,
        )
        from ..models.inline_compute import InlineCompute

        operator = self.operator.value

        operands = []
        for operands_item_data in self.operands:
            operands_item: dict[str, Any] | float | int | str
            if isinstance(operands_item_data, ComposeLiteral):
                operands_item = operands_item_data.to_dict()
            else:
                operands_item = operands_item_data
            operands.append(operands_item)

        output = self.output

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        conditions: list[dict[str, Any]] | None | Unset
        if isinstance(self.conditions, Unset):
            conditions = UNSET
        elif isinstance(self.conditions, list):
            conditions = []
            for conditions_type_0_item_data in self.conditions:
                conditions_type_0_item: dict[str, Any]
                if isinstance(
                    conditions_type_0_item_data, ComposeAttributeCondition
                ) or isinstance(
                    conditions_type_0_item_data, GridGeometrySpatialCondition
                ):
                    conditions_type_0_item = conditions_type_0_item_data.to_dict()
                else:
                    conditions_type_0_item = conditions_type_0_item_data.to_dict()

                conditions.append(conditions_type_0_item)

        else:
            conditions = self.conditions

        else_: dict[str, Any] | float | int | None | str | Unset
        if isinstance(self.else_, Unset):
            else_ = UNSET
        elif isinstance(self.else_, ComposeLiteral) or isinstance(
            self.else_, InlineCompute
        ):
            else_ = self.else_.to_dict()
        else:
            else_ = self.else_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
                "operands": operands,
                "output": output,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if unit is not UNSET:
            field_dict["unit"] = unit
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if else_ is not UNSET:
            field_dict["else"] = else_

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.compose_attribute_condition import ComposeAttributeCondition
        from ..models.compose_literal import ComposeLiteral
        from ..models.grid_feature_spatial_condition import GridFeatureSpatialCondition
        from ..models.grid_geometry_spatial_condition import (
            GridGeometrySpatialCondition,
        )
        from ..models.inline_compute import InlineCompute

        d = dict(src_dict)
        operator = ComposeOperator(d.pop("operator"))

        operands = []
        _operands = d.pop("operands")
        for operands_item_data in _operands:

            def _parse_operands_item(
                data: object,
            ) -> ComposeLiteral | float | int | str:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    operands_item_type_3 = ComposeLiteral.from_dict(data)

                    return operands_item_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(ComposeLiteral | float | int | str, data)

            operands_item = _parse_operands_item(operands_item_data)

            operands.append(operands_item)

        output = d.pop("output")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_conditions(
            data: object,
        ) -> (
            list[
                ComposeAttributeCondition
                | GridFeatureSpatialCondition
                | GridGeometrySpatialCondition
            ]
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                conditions_type_0 = []
                _conditions_type_0 = data
                for conditions_type_0_item_data in _conditions_type_0:

                    def _parse_conditions_type_0_item(
                        data: object,
                    ) -> (
                        ComposeAttributeCondition
                        | GridFeatureSpatialCondition
                        | GridGeometrySpatialCondition
                    ):
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            conditions_type_0_item_type_0 = (
                                ComposeAttributeCondition.from_dict(data)
                            )

                            return conditions_type_0_item_type_0
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            conditions_type_0_item_type_1 = (
                                GridGeometrySpatialCondition.from_dict(data)
                            )

                            return conditions_type_0_item_type_1
                        except (TypeError, ValueError, AttributeError, KeyError):
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        conditions_type_0_item_type_2 = (
                            GridFeatureSpatialCondition.from_dict(data)
                        )

                        return conditions_type_0_item_type_2

                    conditions_type_0_item = _parse_conditions_type_0_item(
                        conditions_type_0_item_data
                    )

                    conditions_type_0.append(conditions_type_0_item)

                return conditions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                list[
                    ComposeAttributeCondition
                    | GridFeatureSpatialCondition
                    | GridGeometrySpatialCondition
                ]
                | None
                | Unset,
                data,
            )

        conditions = _parse_conditions(d.pop("conditions", UNSET))

        def _parse_else_(
            data: object,
        ) -> ComposeLiteral | float | InlineCompute | int | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                else_type_3 = ComposeLiteral.from_dict(data)

                return else_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                else_type_4 = InlineCompute.from_dict(data)

                return else_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                ComposeLiteral | float | InlineCompute | int | None | str | Unset, data
            )

        else_ = _parse_else_(d.pop("else", UNSET))

        compose_compute = cls(
            operator=operator,
            operands=operands,
            output=output,
            name=name,
            description=description,
            unit=unit,
            conditions=conditions,
            else_=else_,
        )

        compose_compute.additional_properties = d
        return compose_compute

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
