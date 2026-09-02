from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.overlap_method import OverlapMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
    from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
    from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreateLayersetRasterizeRequest")


@_attrs_define
class CreateLayersetRasterizeRequest:
    """Request to create a grid by rasterizing a previously-uploaded layerset.

    The referenced layerset must be an existing Feature owned by the caller,
    uploaded via ``POST /domains/{id}/features/layerset``. The worker fetches
    the GeoJSON from GCS at job time; a fresh upload produces a new
    ``feature_id``, so the reference is effectively immutable.

        Attributes:
            layerset_id (str): Feature ID of an existing layerset uploaded for this domain.
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
                `replace`, `multiply`, `divide`, `add`, or `subtract`. A rule with an empty `conditions` list applies its
                actions to the whole grid. See the `GridModification` schema for the full field reference and worked examples.
            extent_buffer_cells (int | Unset): Buffer in result-grid cells around the domain extent. Cells inside the
                buffered extent that fall outside polygon coverage are populated with the rasterizer's fill value. Default 0
                adds no buffer. Maximum: 10 cells. Default: 0.
            alignment (GridAlignmentDomainTarget | GridAlignmentGridTarget | GridAlignmentNativeTarget | Unset): Per-fetch
                alignment target. Default `target="domain"` anchors output cells to the domain origin so cross-source
                composition works by construction. `target="native"` preserves the source pixel anchor. `target="grid"` aligns
                to an existing grid by id.
            overlap_method (OverlapMethod | Unset): Per-cell reduction when multiple polygons of the same ``fuel_type``
                overlap a cell. Applies to ``height`` and the optional bands only —
                ``loading`` is always summed by ``fastfuels_core.rasterize_layerset``
                regardless of this setting.
    """

    layerset_id: str
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
    overlap_method: OverlapMethod | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget

        layerset_id = self.layerset_id

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

        overlap_method: str | Unset = UNSET
        if not isinstance(self.overlap_method, Unset):
            overlap_method = self.overlap_method.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "layerset_id": layerset_id,
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
        if extent_buffer_cells is not UNSET:
            field_dict["extent_buffer_cells"] = extent_buffer_cells
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if overlap_method is not UNSET:
            field_dict["overlap_method"] = overlap_method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
        from ..models.grid_modification import GridModification

        d = dict(src_dict)
        layerset_id = d.pop("layerset_id")

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

        _overlap_method = d.pop("overlap_method", UNSET)
        overlap_method: OverlapMethod | Unset
        if isinstance(_overlap_method, Unset):
            overlap_method = UNSET
        else:
            overlap_method = OverlapMethod(_overlap_method)

        create_layerset_rasterize_request = cls(
            layerset_id=layerset_id,
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
            extent_buffer_cells=extent_buffer_cells,
            alignment=alignment,
            overlap_method=overlap_method,
        )

        create_layerset_rasterize_request.additional_properties = d
        return create_layerset_rasterize_request

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
