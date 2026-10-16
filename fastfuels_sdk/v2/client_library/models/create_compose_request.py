from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compose_compute import ComposeCompute
    from ..models.compose_input import ComposeInput
    from ..models.compose_select import ComposeSelect
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreateComposeRequest")


@_attrs_define
class CreateComposeRequest:
    """Request to create a grid by composing one or more existing grids.

    Attributes:
        inputs (list[ComposeInput]):
        operations (list[ComposeCompute | ComposeSelect]): Select and compute operations, one per output band. Output
            bands follow this order.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        modifications (list[GridModification] | Unset):
    """

    inputs: list[ComposeInput]
    operations: list[ComposeCompute | ComposeSelect]
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.compose_select import ComposeSelect

        inputs = []
        for inputs_item_data in self.inputs:
            inputs_item = inputs_item_data.to_dict()
            inputs.append(inputs_item)

        operations = []
        for operations_item_data in self.operations:
            operations_item: dict[str, Any]
            if isinstance(operations_item_data, ComposeSelect):
                operations_item = operations_item_data.to_dict()
            else:
                operations_item = operations_item_data.to_dict()

            operations.append(operations_item)

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        modifications: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.modifications, Unset):
            modifications = []
            for modifications_item_data in self.modifications:
                modifications_item = modifications_item_data.to_dict()
                modifications.append(modifications_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputs": inputs,
                "operations": operations,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if modifications is not UNSET:
            field_dict["modifications"] = modifications

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.compose_compute import ComposeCompute
        from ..models.compose_input import ComposeInput
        from ..models.compose_select import ComposeSelect
        from ..models.grid_modification import GridModification

        d = dict(src_dict)
        inputs = []
        _inputs = d.pop("inputs")
        for inputs_item_data in _inputs:
            inputs_item = ComposeInput.from_dict(inputs_item_data)

            inputs.append(inputs_item)

        operations = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:

            def _parse_operations_item(data: object) -> ComposeCompute | ComposeSelect:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    operations_item_type_0 = ComposeSelect.from_dict(data)

                    return operations_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                operations_item_type_1 = ComposeCompute.from_dict(data)

                return operations_item_type_1

            operations_item = _parse_operations_item(operations_item_data)

            operations.append(operations_item)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _modifications = d.pop("modifications", UNSET)
        modifications: list[GridModification] | Unset = UNSET
        if _modifications is not UNSET:
            modifications = []
            for modifications_item_data in _modifications:
                modifications_item = GridModification.from_dict(modifications_item_data)

                modifications.append(modifications_item)

        create_compose_request = cls(
            inputs=inputs,
            operations=operations,
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
        )

        create_compose_request.additional_properties = d
        return create_compose_request

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
