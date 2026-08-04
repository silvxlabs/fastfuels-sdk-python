from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.landfire_canopy_fuel_band import LandfireCanopyFuelBand
from ..models.landfire_canopy_version import LandfireCanopyVersion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
    from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
    from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreateLandfireCanopyRequest")


@_attrs_define
class CreateLandfireCanopyRequest:
    """Request to create a grid from LANDFIRE canopy data.

    Returns a grid with one or more continuous canopy bands at 30m
    resolution (CONUS):
    - chm: Canopy height (m)
    - cbd: Canopy bulk density (kg/m**3)
    - cbh: Canopy base height (m)
    - cc:  Canopy cover (%)

    Bands are validated against the canopy band vocabulary and may not be
    duplicated.

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
            extent_buffer_cells (int | Unset): Number of result-grid cells included as a buffer around the domain extent in
                the stored grid. The buffer is measured after the source raster is projected into the domain CRS, so a cell
                means one cell in the returned grid rather than one source raster cell. Provides context for later operations
                (resample, reproject, focal filters, derivative calculations) that are sensitive to edges. Default 0 adds no
                buffer. Maximum: 10 cells. Default: 0.
            alignment (GridAlignmentDomainTarget | GridAlignmentGridTarget | GridAlignmentNativeTarget | Unset): Per-fetch
                alignment target. Default `target="domain"` anchors output cells to the domain origin so cross-source
                composition works by construction. `target="native"` preserves the source pixel anchor. `target="grid"` aligns
                to an existing grid by id.
            version (LandfireCanopyVersion | Unset): Available LANDFIRE canopy data versions.
            bands (list[LandfireCanopyFuelBand] | Unset):
    """

    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    modifications: list[GridModification] | Unset = UNSET
    extent_buffer_cells: int | Unset = 0
    alignment: (
        GridAlignmentDomainTarget
        | GridAlignmentGridTarget
        | GridAlignmentNativeTarget
        | Unset
    ) = UNSET
    version: LandfireCanopyVersion | Unset = UNSET
    bands: list[LandfireCanopyFuelBand] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget

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

        extent_buffer_cells = self.extent_buffer_cells

        alignment: dict[str, Any] | Unset
        if isinstance(self.alignment, Unset):
            alignment = UNSET
        elif isinstance(self.alignment, GridAlignmentDomainTarget) or isinstance(
            self.alignment, GridAlignmentNativeTarget
        ):
            alignment = self.alignment.to_dict()
        else:
            alignment = self.alignment.to_dict()

        version: str | Unset = UNSET
        if not isinstance(self.version, Unset):
            version = self.version.value

        bands: list[str] | Unset = UNSET
        if not isinstance(self.bands, Unset):
            bands = []
            for bands_item_data in self.bands:
                bands_item = bands_item_data.value
                bands.append(bands_item)

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
        if extent_buffer_cells is not UNSET:
            field_dict["extent_buffer_cells"] = extent_buffer_cells
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if version is not UNSET:
            field_dict["version"] = version
        if bands is not UNSET:
            field_dict["bands"] = bands

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
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

        extent_buffer_cells = d.pop("extent_buffer_cells", UNSET)

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

        _version = d.pop("version", UNSET)
        version: LandfireCanopyVersion | Unset
        if isinstance(_version, Unset):
            version = UNSET
        else:
            version = LandfireCanopyVersion(_version)

        _bands = d.pop("bands", UNSET)
        bands: list[LandfireCanopyFuelBand] | Unset = UNSET
        if _bands is not UNSET:
            bands = []
            for bands_item_data in _bands:
                bands_item = LandfireCanopyFuelBand(bands_item_data)

                bands.append(bands_item)

        create_landfire_canopy_request = cls(
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
            extent_buffer_cells=extent_buffer_cells,
            alignment=alignment,
            version=version,
            bands=bands,
        )

        create_landfire_canopy_request.additional_properties = d
        return create_landfire_canopy_request

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
