from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.compose_operator import ComposeOperator

if TYPE_CHECKING:
    from ..models.compose_literal import ComposeLiteral


T = TypeVar("T", bound="InlineCompute")


@_attrs_define
class InlineCompute:
    """A computation body: an operator over operands.

    Usable on its own as a conditional-fallback value; `ComposeCompute`
    extends it with an output target and optional conditions.

        Attributes:
            operator (ComposeOperator): Operators available for compose computations.
            operands (list[ComposeLiteral | float | int | str]):
    """

    operator: ComposeOperator
    operands: list[ComposeLiteral | float | int | str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.compose_literal import ComposeLiteral

        operator = self.operator.value

        operands = []
        for operands_item_data in self.operands:
            operands_item: dict[str, Any] | float | int | str
            if isinstance(operands_item_data, ComposeLiteral):
                operands_item = operands_item_data.to_dict()
            else:
                operands_item = operands_item_data
            operands.append(operands_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
                "operands": operands,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.compose_literal import ComposeLiteral

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

        inline_compute = cls(
            operator=operator,
            operands=operands,
        )

        inline_compute.additional_properties = d
        return inline_compute

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
