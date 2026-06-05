from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.landfire_fccs_version import LandfireFccsVersion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreateLandfireFccsRequest")


@_attrs_define
class CreateLandfireFccsRequest:
    """Request to create a grid from LANDFIRE FCCS.

    Returns a single-band grid with categorical fuelbed IDs.
    To convert IDs to fuel parameters, use /grids/lookup/fccs.

        Attributes:
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            modifications (list[GridModification] | Unset): Rules applied to the grid after it is built from its source.
                Each rule has a list of `conditions` (ANDed together) and a list of `actions` (applied where the conditions
                match). Conditions can be attribute-based (compare a band value) or spatial (test cell location against a
                geometry). Spatial conditions come in two variants discriminated by `source`: `geometry` (inline GeoJSON) or
                `feature` (reference a persisted Feature resource — road, water, layerset — in the same domain by `feature_id`).
                Both spatial variants accept `buffer_m` (meters, applied in the domain's projected CRS) to widen the geometry,
                and `target` (`centroid` or `cell`) to choose which part of the cell is tested. Actions modify band values via
                `replace`, `multiply`, `divide`, `add`, or `subtract`. See the `GridModification` schema for the full field
                reference and worked examples.
            version (LandfireFccsVersion | Unset): Available LANDFIRE FCCS data versions.
            remove_bare_ground (bool | Unset):  Default: False.
    """

    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    version: LandfireFccsVersion | Unset = UNSET
    remove_bare_ground: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        version: str | Unset = UNSET
        if not isinstance(self.version, Unset):
            version = self.version.value

        remove_bare_ground = self.remove_bare_ground

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if modifications is not UNSET:
            field_dict["modifications"] = modifications
        if version is not UNSET:
            field_dict["version"] = version
        if remove_bare_ground is not UNSET:
            field_dict["remove_bare_ground"] = remove_bare_ground

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grid_modification import GridModification

        d = dict(src_dict)
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

        _version = d.pop("version", UNSET)
        version: LandfireFccsVersion | Unset
        if isinstance(_version, Unset):
            version = UNSET
        else:
            version = LandfireFccsVersion(_version)

        remove_bare_ground = d.pop("remove_bare_ground", UNSET)

        create_landfire_fccs_request = cls(
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
            version=version,
            remove_bare_ground=remove_bare_ground,
        )

        create_landfire_fccs_request.additional_properties = d
        return create_landfire_fccs_request

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
