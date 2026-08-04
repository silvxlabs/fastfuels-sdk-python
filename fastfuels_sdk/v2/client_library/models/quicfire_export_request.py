from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.quicfire_export_request_moist_merge import QuicfireExportRequestMoistMerge
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.field_source import FieldSource
    from ..models.quic_fire_export_alignment_domain_target import (
        QUICFireExportAlignmentDomainTarget,
    )
    from ..models.quic_fire_export_alignment_grid_target import (
        QUICFireExportAlignmentGridTarget,
    )


T = TypeVar("T", bound="QuicfireExportRequest")


@_attrs_define
class QuicfireExportRequest:
    """Request body for creating a QUIC-Fire combined export.

    Five required roles produce `treesrhof.dat`, `treesmoist.dat`, and
    `treesfueldepth.dat`. `topography` (optional) produces `topo.dat`. The
    SAVR pair (optional, both-or-neither) produces `treesss.dat`.

    The fire grid is defined by the `alignment` field — either the Domain
    bounding box padded to `(dx, dy)` (with `dz` vertical), or the lattice
    of an existing grid. Every role grid must be lattice-aligned to this
    fire grid and cover its full extent; otherwise the request is rejected.
    The exporter only crops oversized roles by integer slicing — it never
    resamples or reprojects.

    The output resolution is set here, on the export, via `alignment.dx`/`dy`
    (default 2 m, QUIC-Fire's recommended value). It is a separate setting
    from the resolution of each grid you built — changing your grids does not
    change the export, and vice versa. Because the exporter never resamples,
    every role grid must already be built at the fire-grid resolution. To
    export at 1 m, for example, set `dx`/`dy` to 1 and build all role grids at
    1 m (2D grids at 1 m via their `alignment.resolution`, and the 3D tree
    grid at 1 m via `resolution.horizontal` — 3D grids cannot be resampled).
    The same holds vertically: `alignment.dz` must equal the 3D tree grid's
    `resolution.vertical`, or the request is rejected with 422.

        Attributes:
            canopy_bulk_density (FieldSource): A single physical quantity drawn from one band on one grid.

                Every per-role input to the QUIC-Fire export uses this shape so the schema
                is uniform across roles. The forward path for `nfuel>1` (when QUIC-Fire's
                multi-fuel-type capability becomes relevant) is to allow each per-fuel-type
                role to accept `FieldSource | dict[FuelType, FieldSource]`; today's scalar
                requests keep working unchanged when that lands.
            canopy_moisture (FieldSource): A single physical quantity drawn from one band on one grid.

                Every per-role input to the QUIC-Fire export uses this shape so the schema
                is uniform across roles. The forward path for `nfuel>1` (when QUIC-Fire's
                multi-fuel-type capability becomes relevant) is to allow each per-fuel-type
                role to accept `FieldSource | dict[FuelType, FieldSource]`; today's scalar
                requests keep working unchanged when that lands.
            surface_fuel_load (FieldSource): A single physical quantity drawn from one band on one grid.

                Every per-role input to the QUIC-Fire export uses this shape so the schema
                is uniform across roles. The forward path for `nfuel>1` (when QUIC-Fire's
                multi-fuel-type capability becomes relevant) is to allow each per-fuel-type
                role to accept `FieldSource | dict[FuelType, FieldSource]`; today's scalar
                requests keep working unchanged when that lands.
            surface_fuel_depth (FieldSource): A single physical quantity drawn from one band on one grid.

                Every per-role input to the QUIC-Fire export uses this shape so the schema
                is uniform across roles. The forward path for `nfuel>1` (when QUIC-Fire's
                multi-fuel-type capability becomes relevant) is to allow each per-fuel-type
                role to accept `FieldSource | dict[FuelType, FieldSource]`; today's scalar
                requests keep working unchanged when that lands.
            surface_moisture (FieldSource): A single physical quantity drawn from one band on one grid.

                Every per-role input to the QUIC-Fire export uses this shape so the schema
                is uniform across roles. The forward path for `nfuel>1` (when QUIC-Fire's
                multi-fuel-type capability becomes relevant) is to allow each per-fuel-type
                role to accept `FieldSource | dict[FuelType, FieldSource]`; today's scalar
                requests keep working unchanged when that lands.
            alignment (QUICFireExportAlignmentDomainTarget | QUICFireExportAlignmentGridTarget | Unset): How the fire grid
                lattice is defined. Discriminated by `target`: `'domain'` (default) pads the Domain bbox to `(dx, dy)`; `'grid'`
                matches an existing grid's lattice exactly. Omit for the default Domain-anchored 2 m / 1 m fire grid.
            canopy_savr (FieldSource | None | Unset): 3D canopy SAVR (1/m), optional. When provided, must be paired with
                `surface_savr`; together they produce `treesss.dat` in the output zip.
            surface_savr (FieldSource | None | Unset): 2D surface SAVR (1/m), optional. Pairs with `canopy_savr`.
            topography (FieldSource | None | Unset): 2D elevation (m), optional. When provided, produces `topo.dat`.
            rhof_merge (Literal['sum'] | Unset): How to combine canopy and surface bulk density at the bottom slab (k=0).
                Currently only 'sum' is supported: `merged[0] = canopy[0] + surface_load / dz`. Mass-additive. Default: 'sum'.
            moist_merge (QuicfireExportRequestMoistMerge | Unset): How to combine canopy and surface fuel moisture at the
                bottom slab (k=0). `'max'` (default, v1-parity): `merged[0] = max(canopy_moist[0], surface_moist)`.
                `'weighted_avg'`: `merged[0] = (canopy_rhof[0] * canopy_moist[0] + surface_rhof_layer * surface_moist) /
                (canopy_rhof[0] + surface_rhof_layer)` (both moistures already converted to fraction). Default:
                QuicfireExportRequestMoistMerge.MAX.
            savr_merge (Literal['weighted_avg'] | Unset): How to combine canopy and surface SAVR at the bottom slab.
                Currently only 'weighted_avg' is supported (mass-weighted SAVR, then converted to particle size scale `2/SAVR`
                before write). Only applies when both `canopy_savr` and `surface_savr` are set. Default: 'weighted_avg'.
            expiration_days (int | Unset): Days until the signed download URL expires (max 7). Default: 7.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
    """

    canopy_bulk_density: FieldSource
    canopy_moisture: FieldSource
    surface_fuel_load: FieldSource
    surface_fuel_depth: FieldSource
    surface_moisture: FieldSource
    alignment: (
        QUICFireExportAlignmentDomainTarget | QUICFireExportAlignmentGridTarget | Unset
    ) = UNSET
    canopy_savr: FieldSource | None | Unset = UNSET
    surface_savr: FieldSource | None | Unset = UNSET
    topography: FieldSource | None | Unset = UNSET
    rhof_merge: Literal["sum"] | Unset = "sum"
    moist_merge: QuicfireExportRequestMoistMerge | Unset = (
        QuicfireExportRequestMoistMerge.MAX
    )
    savr_merge: Literal["weighted_avg"] | Unset = "weighted_avg"
    expiration_days: int | Unset = 7
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.field_source import FieldSource
        from ..models.quic_fire_export_alignment_domain_target import (
            QUICFireExportAlignmentDomainTarget,
        )

        canopy_bulk_density = self.canopy_bulk_density.to_dict()

        canopy_moisture = self.canopy_moisture.to_dict()

        surface_fuel_load = self.surface_fuel_load.to_dict()

        surface_fuel_depth = self.surface_fuel_depth.to_dict()

        surface_moisture = self.surface_moisture.to_dict()

        alignment: dict[str, Any] | Unset
        if isinstance(self.alignment, Unset):
            alignment = UNSET
        elif isinstance(self.alignment, QUICFireExportAlignmentDomainTarget):
            alignment = self.alignment.to_dict()
        else:
            alignment = self.alignment.to_dict()

        canopy_savr: dict[str, Any] | None | Unset
        if isinstance(self.canopy_savr, Unset):
            canopy_savr = UNSET
        elif isinstance(self.canopy_savr, FieldSource):
            canopy_savr = self.canopy_savr.to_dict()
        else:
            canopy_savr = self.canopy_savr

        surface_savr: dict[str, Any] | None | Unset
        if isinstance(self.surface_savr, Unset):
            surface_savr = UNSET
        elif isinstance(self.surface_savr, FieldSource):
            surface_savr = self.surface_savr.to_dict()
        else:
            surface_savr = self.surface_savr

        topography: dict[str, Any] | None | Unset
        if isinstance(self.topography, Unset):
            topography = UNSET
        elif isinstance(self.topography, FieldSource):
            topography = self.topography.to_dict()
        else:
            topography = self.topography

        rhof_merge = self.rhof_merge

        moist_merge: str | Unset = UNSET
        if not isinstance(self.moist_merge, Unset):
            moist_merge = self.moist_merge.value

        savr_merge = self.savr_merge

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
                "canopy_bulk_density": canopy_bulk_density,
                "canopy_moisture": canopy_moisture,
                "surface_fuel_load": surface_fuel_load,
                "surface_fuel_depth": surface_fuel_depth,
                "surface_moisture": surface_moisture,
            }
        )
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if canopy_savr is not UNSET:
            field_dict["canopy_savr"] = canopy_savr
        if surface_savr is not UNSET:
            field_dict["surface_savr"] = surface_savr
        if topography is not UNSET:
            field_dict["topography"] = topography
        if rhof_merge is not UNSET:
            field_dict["rhof_merge"] = rhof_merge
        if moist_merge is not UNSET:
            field_dict["moist_merge"] = moist_merge
        if savr_merge is not UNSET:
            field_dict["savr_merge"] = savr_merge
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
        from ..models.field_source import FieldSource
        from ..models.quic_fire_export_alignment_domain_target import (
            QUICFireExportAlignmentDomainTarget,
        )
        from ..models.quic_fire_export_alignment_grid_target import (
            QUICFireExportAlignmentGridTarget,
        )

        d = dict(src_dict)
        canopy_bulk_density = FieldSource.from_dict(d.pop("canopy_bulk_density"))

        canopy_moisture = FieldSource.from_dict(d.pop("canopy_moisture"))

        surface_fuel_load = FieldSource.from_dict(d.pop("surface_fuel_load"))

        surface_fuel_depth = FieldSource.from_dict(d.pop("surface_fuel_depth"))

        surface_moisture = FieldSource.from_dict(d.pop("surface_moisture"))

        def _parse_alignment(
            data: object,
        ) -> (
            QUICFireExportAlignmentDomainTarget
            | QUICFireExportAlignmentGridTarget
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                alignment_type_0 = QUICFireExportAlignmentDomainTarget.from_dict(data)

                return alignment_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            alignment_type_1 = QUICFireExportAlignmentGridTarget.from_dict(data)

            return alignment_type_1

        alignment = _parse_alignment(d.pop("alignment", UNSET))

        def _parse_canopy_savr(data: object) -> FieldSource | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                canopy_savr_type_0 = FieldSource.from_dict(data)

                return canopy_savr_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FieldSource | None | Unset, data)

        canopy_savr = _parse_canopy_savr(d.pop("canopy_savr", UNSET))

        def _parse_surface_savr(data: object) -> FieldSource | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                surface_savr_type_0 = FieldSource.from_dict(data)

                return surface_savr_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FieldSource | None | Unset, data)

        surface_savr = _parse_surface_savr(d.pop("surface_savr", UNSET))

        def _parse_topography(data: object) -> FieldSource | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                topography_type_0 = FieldSource.from_dict(data)

                return topography_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FieldSource | None | Unset, data)

        topography = _parse_topography(d.pop("topography", UNSET))

        rhof_merge = cast(Literal["sum"] | Unset, d.pop("rhof_merge", UNSET))
        if rhof_merge != "sum" and not isinstance(rhof_merge, Unset):
            raise ValueError(f"rhof_merge must match const 'sum', got '{rhof_merge}'")

        _moist_merge = d.pop("moist_merge", UNSET)
        moist_merge: QuicfireExportRequestMoistMerge | Unset
        if isinstance(_moist_merge, Unset):
            moist_merge = UNSET
        else:
            moist_merge = QuicfireExportRequestMoistMerge(_moist_merge)

        savr_merge = cast(Literal["weighted_avg"] | Unset, d.pop("savr_merge", UNSET))
        if savr_merge != "weighted_avg" and not isinstance(savr_merge, Unset):
            raise ValueError(
                f"savr_merge must match const 'weighted_avg', got '{savr_merge}'"
            )

        expiration_days = d.pop("expiration_days", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        quicfire_export_request = cls(
            canopy_bulk_density=canopy_bulk_density,
            canopy_moisture=canopy_moisture,
            surface_fuel_load=surface_fuel_load,
            surface_fuel_depth=surface_fuel_depth,
            surface_moisture=surface_moisture,
            alignment=alignment,
            canopy_savr=canopy_savr,
            surface_savr=surface_savr,
            topography=topography,
            rhof_merge=rhof_merge,
            moist_merge=moist_merge,
            savr_merge=savr_merge,
            expiration_days=expiration_days,
            name=name,
            description=description,
            tags=tags,
        )

        quicfire_export_request.additional_properties = d
        return quicfire_export_request

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
