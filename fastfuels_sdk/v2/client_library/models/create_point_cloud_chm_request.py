from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chm_max_aggregation import ChmMaxAggregation
    from ..models.chm_mean_aggregation import ChmMeanAggregation
    from ..models.chm_median_aggregation import ChmMedianAggregation
    from ..models.chm_percentile_aggregation import ChmPercentileAggregation
    from ..models.chm_spike_filter import ChmSpikeFilter
    from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
    from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
    from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
    from ..models.grid_modification import GridModification


T = TypeVar("T", bound="CreatePointCloudChmRequest")


@_attrs_define
class CreatePointCloudChmRequest:
    """Request to create a canopy height model grid from a point cloud.

    Returns a grid with a single continuous band:
    - chm: Canopy height in meters

    The point cloud must be airborne (`type: als`) and `completed`. Cell size
    comes from `alignment.resolution`, defaulting to 1 m — unlike the
    raster-backed canopy sources there is no source pixel size to inherit.

        Attributes:
            source_point_cloud_id (str): ID of the point cloud to rasterize. Must be an ALS cloud in this domain.
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
            spike_filter (ChmSpikeFilter | None | Unset): Removal of lone spurious returns. Omit for the defaults; send
                `null` to keep every return, leaving unclassified noise in the grid.
            aggregation (ChmMaxAggregation | ChmMeanAggregation | ChmMedianAggregation | ChmPercentileAggregation | Unset):
                Statistic each cell reduces the heights above ground of its returns with. Carries `percentile` only on `method:
                percentile`.
    """

    source_point_cloud_id: str
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
    spike_filter: ChmSpikeFilter | None | Unset = UNSET
    aggregation: (
        ChmMaxAggregation
        | ChmMeanAggregation
        | ChmMedianAggregation
        | ChmPercentileAggregation
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chm_max_aggregation import ChmMaxAggregation
        from ..models.chm_mean_aggregation import ChmMeanAggregation
        from ..models.chm_median_aggregation import ChmMedianAggregation
        from ..models.chm_spike_filter import ChmSpikeFilter
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget

        source_point_cloud_id = self.source_point_cloud_id

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

        spike_filter: dict[str, Any] | None | Unset
        if isinstance(self.spike_filter, Unset):
            spike_filter = UNSET
        elif isinstance(self.spike_filter, ChmSpikeFilter):
            spike_filter = self.spike_filter.to_dict()
        else:
            spike_filter = self.spike_filter

        aggregation: dict[str, Any] | Unset
        if isinstance(self.aggregation, Unset):
            aggregation = UNSET
        elif (
            isinstance(self.aggregation, ChmMaxAggregation)
            or isinstance(self.aggregation, ChmMeanAggregation)
            or isinstance(self.aggregation, ChmMedianAggregation)
        ):
            aggregation = self.aggregation.to_dict()
        else:
            aggregation = self.aggregation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_point_cloud_id": source_point_cloud_id,
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
        if spike_filter is not UNSET:
            field_dict["spike_filter"] = spike_filter
        if aggregation is not UNSET:
            field_dict["aggregation"] = aggregation

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.chm_max_aggregation import ChmMaxAggregation
        from ..models.chm_mean_aggregation import ChmMeanAggregation
        from ..models.chm_median_aggregation import ChmMedianAggregation
        from ..models.chm_percentile_aggregation import ChmPercentileAggregation
        from ..models.chm_spike_filter import ChmSpikeFilter
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
        from ..models.grid_modification import GridModification

        d = dict(src_dict)
        source_point_cloud_id = d.pop("source_point_cloud_id")

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

        def _parse_spike_filter(data: object) -> ChmSpikeFilter | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                spike_filter_type_0 = ChmSpikeFilter.from_dict(data)

                return spike_filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ChmSpikeFilter | None | Unset, data)

        spike_filter = _parse_spike_filter(d.pop("spike_filter", UNSET))

        def _parse_aggregation(
            data: object,
        ) -> (
            ChmMaxAggregation
            | ChmMeanAggregation
            | ChmMedianAggregation
            | ChmPercentileAggregation
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregation_type_0 = ChmMaxAggregation.from_dict(data)

                return aggregation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregation_type_1 = ChmMeanAggregation.from_dict(data)

                return aggregation_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregation_type_2 = ChmMedianAggregation.from_dict(data)

                return aggregation_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            aggregation_type_3 = ChmPercentileAggregation.from_dict(data)

            return aggregation_type_3

        aggregation = _parse_aggregation(d.pop("aggregation", UNSET))

        create_point_cloud_chm_request = cls(
            source_point_cloud_id=source_point_cloud_id,
            name=name,
            description=description,
            tags=tags,
            modifications=modifications,
            extent_buffer_cells=extent_buffer_cells,
            alignment=alignment,
            spike_filter=spike_filter,
            aggregation=aggregation,
        )

        create_point_cloud_chm_request.additional_properties = d
        return create_point_cloud_chm_request

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
