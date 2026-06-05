from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.grid_modification import GridModification
    from ..models.uniform_band_input import UniformBandInput


T = TypeVar("T", bound="CreateUniformRequest")


@_attrs_define
class CreateUniformRequest:
    """Request to create a uniform (constant-value) grid.

    Each band fills the entire domain with a single value at the specified
    resolution. No default resolution — it must be explicitly provided since
    uniform grids have no "native resolution."

        Attributes:
            resolution (float): Grid resolution in meters
            bands (list[UniformBandInput]):
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
    """

    resolution: float
    bands: list[UniformBandInput]
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resolution = self.resolution

        bands = []
        for bands_item_data in self.bands:
            bands_item = bands_item_data.to_dict()
            bands.append(bands_item)

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
                "resolution": resolution,
                "bands": bands,
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grid_modification import GridModification
        from ..models.uniform_band_input import UniformBandInput

        d = dict(src_dict)
        resolution = d.pop("resolution")

        bands = []
        _bands = d.pop("bands")
        for bands_item_data in _bands:
            bands_item = UniformBandInput.from_dict(bands_item_data)

            bands.append(bands_item)

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

        create_uniform_request = cls(
            resolution=resolution,
            bands=bands,
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
        )

        create_uniform_request.additional_properties = d
        return create_uniform_request

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
