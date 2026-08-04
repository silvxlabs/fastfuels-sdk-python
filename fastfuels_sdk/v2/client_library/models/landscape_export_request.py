from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.landscape_export_request_fire_behavior_fuel_model import (
    LandscapeExportRequestFireBehaviorFuelModel,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.landscape_export_alignment_domain_target import (
        LandscapeExportAlignmentDomainTarget,
    )
    from ..models.landscape_export_alignment_grid_target import (
        LandscapeExportAlignmentGridTarget,
    )
    from ..models.landscape_field_source import LandscapeFieldSource


T = TypeVar("T", bound="LandscapeExportRequest")


@_attrs_define
class LandscapeExportRequest:
    """Request body for creating a landscape export.

    Eight required roles produce an 8-band landscape GeoTIFF in LANDFIRE band
    order: elevation, slope, aspect, fuel model, canopy cover, canopy height,
    canopy base height, canopy bulk density. This is the shape modern fire
    behavior tools consume — IFTDSS requires all eight bands for upload.

    The landscape lattice is defined by the `alignment` field — either the
    Domain bounding box tiled at `resolution` (default 30 m, LANDFIRE-native),
    or the lattice of an existing grid. Every role grid must be lattice-aligned
    to the landscape and cover its full extent; otherwise the request is
    rejected with 422. The exporter only crops oversized roles by integer
    slicing — it never resamples or reprojects. To change a grid's resolution
    or anchor, use `POST /v2/domains/{domain_id}/grids/{grid_id}/resample`.

        Attributes:
            fire_behavior_fuel_model (LandscapeExportRequestFireBehaviorFuelModel): How the `fuel_model` band's codes should
                be interpreted: `'fbfm40'` (Scott-Burgan 40) or `'fbfm13'` (Anderson 13). Recorded in the landscape file so fire
                behavior tools apply the right classification.
            elevation (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            slope (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            aspect (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            fuel_model (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            canopy_cover (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            canopy_height (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            canopy_base_height (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            canopy_bulk_density (LandscapeFieldSource): A single landscape band drawn from one band on one grid.
            alignment (LandscapeExportAlignmentDomainTarget | LandscapeExportAlignmentGridTarget | Unset): How the landscape
                lattice is defined. Discriminated by `target`: `'domain'` (default) tiles the Domain bbox at `resolution`;
                `'grid'` matches an existing grid's lattice exactly. Omit for the default Domain-anchored 30 m landscape.
            expiration_days (int | Unset): Days until the signed download URL expires (max 7). Default: 7.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
    """

    fire_behavior_fuel_model: LandscapeExportRequestFireBehaviorFuelModel
    elevation: LandscapeFieldSource
    slope: LandscapeFieldSource
    aspect: LandscapeFieldSource
    fuel_model: LandscapeFieldSource
    canopy_cover: LandscapeFieldSource
    canopy_height: LandscapeFieldSource
    canopy_base_height: LandscapeFieldSource
    canopy_bulk_density: LandscapeFieldSource
    alignment: (
        LandscapeExportAlignmentDomainTarget
        | LandscapeExportAlignmentGridTarget
        | Unset
    ) = UNSET
    expiration_days: int | Unset = 7
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.landscape_export_alignment_domain_target import (
            LandscapeExportAlignmentDomainTarget,
        )

        fire_behavior_fuel_model = self.fire_behavior_fuel_model.value

        elevation = self.elevation.to_dict()

        slope = self.slope.to_dict()

        aspect = self.aspect.to_dict()

        fuel_model = self.fuel_model.to_dict()

        canopy_cover = self.canopy_cover.to_dict()

        canopy_height = self.canopy_height.to_dict()

        canopy_base_height = self.canopy_base_height.to_dict()

        canopy_bulk_density = self.canopy_bulk_density.to_dict()

        alignment: dict[str, Any] | Unset
        if isinstance(self.alignment, Unset):
            alignment = UNSET
        elif isinstance(self.alignment, LandscapeExportAlignmentDomainTarget):
            alignment = self.alignment.to_dict()
        else:
            alignment = self.alignment.to_dict()

        expiration_days = self.expiration_days

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fire_behavior_fuel_model": fire_behavior_fuel_model,
                "elevation": elevation,
                "slope": slope,
                "aspect": aspect,
                "fuel_model": fuel_model,
                "canopy_cover": canopy_cover,
                "canopy_height": canopy_height,
                "canopy_base_height": canopy_base_height,
                "canopy_bulk_density": canopy_bulk_density,
            }
        )
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if expiration_days is not UNSET:
            field_dict["expiration_days"] = expiration_days
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.landscape_export_alignment_domain_target import (
            LandscapeExportAlignmentDomainTarget,
        )
        from ..models.landscape_export_alignment_grid_target import (
            LandscapeExportAlignmentGridTarget,
        )
        from ..models.landscape_field_source import LandscapeFieldSource

        d = dict(src_dict)
        fire_behavior_fuel_model = LandscapeExportRequestFireBehaviorFuelModel(
            d.pop("fire_behavior_fuel_model")
        )

        elevation = LandscapeFieldSource.from_dict(d.pop("elevation"))

        slope = LandscapeFieldSource.from_dict(d.pop("slope"))

        aspect = LandscapeFieldSource.from_dict(d.pop("aspect"))

        fuel_model = LandscapeFieldSource.from_dict(d.pop("fuel_model"))

        canopy_cover = LandscapeFieldSource.from_dict(d.pop("canopy_cover"))

        canopy_height = LandscapeFieldSource.from_dict(d.pop("canopy_height"))

        canopy_base_height = LandscapeFieldSource.from_dict(d.pop("canopy_base_height"))

        canopy_bulk_density = LandscapeFieldSource.from_dict(
            d.pop("canopy_bulk_density")
        )

        def _parse_alignment(
            data: object,
        ) -> (
            LandscapeExportAlignmentDomainTarget
            | LandscapeExportAlignmentGridTarget
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                alignment_type_0 = LandscapeExportAlignmentDomainTarget.from_dict(data)

                return alignment_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            alignment_type_1 = LandscapeExportAlignmentGridTarget.from_dict(data)

            return alignment_type_1

        alignment = _parse_alignment(d.pop("alignment", UNSET))

        expiration_days = d.pop("expiration_days", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        landscape_export_request = cls(
            fire_behavior_fuel_model=fire_behavior_fuel_model,
            elevation=elevation,
            slope=slope,
            aspect=aspect,
            fuel_model=fuel_model,
            canopy_cover=canopy_cover,
            canopy_height=canopy_height,
            canopy_base_height=canopy_base_height,
            canopy_bulk_density=canopy_bulk_density,
            alignment=alignment,
            expiration_days=expiration_days,
            name=name,
            description=description,
            tags=tags,
        )

        landscape_export_request.additional_properties = d
        return landscape_export_request

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
