from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fccs_lookup_band import FccsLookupBand
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreateFccsLookupRequest")


@_attrs_define
class CreateFccsLookupRequest:
    """Request to create a grid by looking up FCCS fuel parameters.

    Unlike entry-point grid creation requests, domain_id is not required
    because derived grids carry the same domain reference as their source.

        Attributes:
            source_grid_id (str): Grid containing FCCS codes
            bands (list[FccsLookupBand]):
            source_band (str | Unset): Band in source grid containing FCCS codes Default: 'fccs'.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            modifications (list[GridModification] | Unset):
    """

    source_grid_id: str
    bands: list[FccsLookupBand]
    source_band: str | Unset = "fccs"
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_grid_id = self.source_grid_id

        bands = []
        for bands_item_data in self.bands:
            bands_item = bands_item_data.value
            bands.append(bands_item)

        source_band = self.source_band

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
                "bands": bands,
            }
        )
        if source_band is not UNSET:
            field_dict["source_band"] = source_band
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
        from ..models.grid_modification import GridModification

        d = dict(src_dict)
        source_grid_id = d.pop("source_grid_id")

        bands = []
        _bands = d.pop("bands")
        for bands_item_data in _bands:
            bands_item = FccsLookupBand(bands_item_data)

            bands.append(bands_item)

        source_band = d.pop("source_band", UNSET)

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

        create_fccs_lookup_request = cls(
            source_grid_id=source_grid_id,
            bands=bands,
            source_band=source_band,
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
        )

        create_fccs_lookup_request.additional_properties = d
        return create_fccs_lookup_request

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
