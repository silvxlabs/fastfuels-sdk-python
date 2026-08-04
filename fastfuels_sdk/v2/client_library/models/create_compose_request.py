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
        select (list[ComposeSelect] | Unset):
        compute (list[ComposeCompute] | Unset):
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        modifications (list[GridModification] | Unset):
    """

    inputs: list[ComposeInput]
    select: list[ComposeSelect] | Unset = UNSET
    compute: list[ComposeCompute] | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inputs = []
        for inputs_item_data in self.inputs:
            inputs_item = inputs_item_data.to_dict()
            inputs.append(inputs_item)

        select: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.select, Unset):
            select = []
            for select_item_data in self.select:
                select_item = select_item_data.to_dict()
                select.append(select_item)

        compute: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.compute, Unset):
            compute = []
            for compute_item_data in self.compute:
                compute_item = compute_item_data.to_dict()
                compute.append(compute_item)

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
            }
        )
        if select is not UNSET:
            field_dict["select"] = select
        if compute is not UNSET:
            field_dict["compute"] = compute
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

        _select = d.pop("select", UNSET)
        select: list[ComposeSelect] | Unset = UNSET
        if _select is not UNSET:
            select = []
            for select_item_data in _select:
                select_item = ComposeSelect.from_dict(select_item_data)

                select.append(select_item)

        _compute = d.pop("compute", UNSET)
        compute: list[ComposeCompute] | Unset = UNSET
        if _compute is not UNSET:
            compute = []
            for compute_item_data in _compute:
                compute_item = ComposeCompute.from_dict(compute_item_data)

                compute.append(compute_item)

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
            select=select,
            compute=compute,
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
