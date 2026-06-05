from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_resample_request_method_overrides import (
        CreateResampleRequestMethodOverrides,
    )
    from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
    from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
    from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreateResampleRequest")


@_attrs_define
class CreateResampleRequest:
    """Request to create a grid by resampling an existing grid.

    Unlike entry-point grid creation requests, ``domain_id`` is not required
    because derived grids carry the same domain reference as their source.

    The ``alignment`` field controls the output lattice. ``alignment.resolution``
    is required for ``target="domain"`` and ``target="native"``; for
    ``target="grid"`` it is optional (defaults to the target grid's exact
    transform/shape; if supplied, keeps the target's CRS and origin and
    recomputes shape at the new cell size).

        Attributes:
            source_grid_id (str): Grid to resample
            alignment (GridAlignmentDomainTarget | GridAlignmentGridTarget | GridAlignmentNativeTarget | Unset): Output
                alignment target. Default `target="domain"` anchors the resampled grid to the domain origin.
            method_overrides (CreateResampleRequestMethodOverrides | Unset): Per-band resampling method overrides keyed by
                band key. Wins over ``alignment.method`` for the listed bands. Useful for using nearest-neighbor on categorical
                bands while using bilinear on continuous bands.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            modifications (list[GridModification] | Unset):
    """

    source_grid_id: str
    alignment: (
        GridAlignmentDomainTarget
        | GridAlignmentGridTarget
        | GridAlignmentNativeTarget
        | Unset
    ) = UNSET
    method_overrides: CreateResampleRequestMethodOverrides | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget

        source_grid_id = self.source_grid_id

        alignment: dict[str, Any] | Unset
        if isinstance(self.alignment, Unset):
            alignment = UNSET
        elif isinstance(self.alignment, GridAlignmentDomainTarget):
            alignment = self.alignment.to_dict()
        elif isinstance(self.alignment, GridAlignmentNativeTarget):
            alignment = self.alignment.to_dict()
        else:
            alignment = self.alignment.to_dict()

        method_overrides: dict[str, Any] | Unset = UNSET
        if not isinstance(self.method_overrides, Unset):
            method_overrides = self.method_overrides.to_dict()

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
                "source_grid_id": source_grid_id,
            }
        )
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if method_overrides is not UNSET:
            field_dict["method_overrides"] = method_overrides
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_resample_request_method_overrides import (
            CreateResampleRequestMethodOverrides,
        )
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
        from ..models.grid_modification import GridModification

        d = dict(src_dict)
        source_grid_id = d.pop("source_grid_id")

        def _parse_alignment(
            data: object,
        ) -> (
            GridAlignmentDomainTarget
            | GridAlignmentGridTarget
            | GridAlignmentNativeTarget
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                alignment_type_0 = GridAlignmentDomainTarget.from_dict(data)

                return alignment_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                alignment_type_1 = GridAlignmentNativeTarget.from_dict(data)

                return alignment_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            alignment_type_2 = GridAlignmentGridTarget.from_dict(data)

            return alignment_type_2

        alignment = _parse_alignment(d.pop("alignment", UNSET))

        _method_overrides = d.pop("method_overrides", UNSET)
        method_overrides: CreateResampleRequestMethodOverrides | Unset
        if isinstance(_method_overrides, Unset):
            method_overrides = UNSET
        else:
            method_overrides = CreateResampleRequestMethodOverrides.from_dict(
                _method_overrides
            )

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

        create_resample_request = cls(
            source_grid_id=source_grid_id,
            alignment=alignment,
            method_overrides=method_overrides,
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
        )

        create_resample_request.additional_properties = d
        return create_resample_request

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
