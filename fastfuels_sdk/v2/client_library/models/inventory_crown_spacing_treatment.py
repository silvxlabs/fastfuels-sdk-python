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

from ..models.inventory_crown_spacing_rank import InventoryCrownSpacingRank
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.canopy_allometry_max_crown_radius_source import (
        CanopyAllometryMaxCrownRadiusSource,
    )
    from ..models.inventory_column_max_crown_radius_source import (
        InventoryColumnMaxCrownRadiusSource,
    )
    from ..models.inventory_feature_spatial_condition import (
        InventoryFeatureSpatialCondition,
    )
    from ..models.inventory_geometry_spatial_condition import (
        InventoryGeometrySpatialCondition,
    )


T = TypeVar("T", bound="InventoryCrownSpacingTreatment")


@_attrs_define
class InventoryCrownSpacingTreatment:
    """Thin to a minimum crown spacing.

    Leaves every retained crown at least ``value`` apart, edge to edge, in plan
    view. Trees are visited from the largest ``rank_by`` value down, and each is
    kept only if its crown clears every crown already kept.

    With ``conditions``, only trees whose stem is in the region can be removed.
    Trees outside the region are never removed, but trees inside it must still
    clear their crowns.

        Attributes:
            value (float): Minimum horizontal gap between retained crowns, crown edge to crown edge, in m unless `unit` is
                set.
            unit (None | str | Unset): Optional unit for `value`. Must be canonical and dimensionally compatible with the
                metric's native unit; converted before the treatment is applied.
            conditions (list[InventoryFeatureSpatialCondition | InventoryGeometrySpatialCondition] | Unset): Spatial
                conditions restricting the treatment to a region (within/outside/intersects a geometry or Feature). An empty
                list applies the treatment to the entire inventory.
            metric (Literal['crown_spacing'] | Unset):  Default: 'crown_spacing'.
            rank_by (InventoryCrownSpacingRank | Unset): Column that decides which tree survives a crown-spacing conflict.

                - dbh: the larger diameter is kept
                - height: the taller tree is kept
            max_crown_radius_source (CanopyAllometryMaxCrownRadiusSource | InventoryColumnMaxCrownRadiusSource | Unset):
                Source of each tree's crown radius. Defaults to the `purves` allometry, the same default as tree voxelization.
                Set `{"type": "allometry", "equations": "crookston_stage"}` for FuelCalc crown widths, or `{"type":
                "inventory_column", "column": "crown_radius"}` to read a measured radius in meters. Trees with no value in the
                column use their `purves` radius. To keep thinned crowns from overlapping in a voxelized or canopy grid, build
                the grid with the same radius source.
    """

    value: float
    unit: None | str | Unset = UNSET
    conditions: (
        list[InventoryFeatureSpatialCondition | InventoryGeometrySpatialCondition]
        | Unset
    ) = UNSET
    metric: Literal["crown_spacing"] | Unset = "crown_spacing"
    rank_by: InventoryCrownSpacingRank | Unset = UNSET
    max_crown_radius_source: (
        CanopyAllometryMaxCrownRadiusSource
        | InventoryColumnMaxCrownRadiusSource
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.canopy_allometry_max_crown_radius_source import (
            CanopyAllometryMaxCrownRadiusSource,
        )
        from ..models.inventory_geometry_spatial_condition import (
            InventoryGeometrySpatialCondition,
        )

        value = self.value

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        conditions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                conditions_item: dict[str, Any]
                if isinstance(conditions_item_data, InventoryGeometrySpatialCondition):
                    conditions_item = conditions_item_data.to_dict()
                else:
                    conditions_item = conditions_item_data.to_dict()

                conditions.append(conditions_item)

        metric = self.metric

        rank_by: str | Unset = UNSET
        if not isinstance(self.rank_by, Unset):
            rank_by = self.rank_by.value

        max_crown_radius_source: dict[str, Any] | Unset
        if isinstance(self.max_crown_radius_source, Unset):
            max_crown_radius_source = UNSET
        elif isinstance(
            self.max_crown_radius_source, CanopyAllometryMaxCrownRadiusSource
        ):
            max_crown_radius_source = self.max_crown_radius_source.to_dict()
        else:
            max_crown_radius_source = self.max_crown_radius_source.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if metric is not UNSET:
            field_dict["metric"] = metric
        if rank_by is not UNSET:
            field_dict["rank_by"] = rank_by
        if max_crown_radius_source is not UNSET:
            field_dict["max_crown_radius_source"] = max_crown_radius_source

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.canopy_allometry_max_crown_radius_source import (
            CanopyAllometryMaxCrownRadiusSource,
        )
        from ..models.inventory_column_max_crown_radius_source import (
            InventoryColumnMaxCrownRadiusSource,
        )
        from ..models.inventory_feature_spatial_condition import (
            InventoryFeatureSpatialCondition,
        )
        from ..models.inventory_geometry_spatial_condition import (
            InventoryGeometrySpatialCondition,
        )

        d = dict(src_dict)
        value = d.pop("value")

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        _conditions = d.pop("conditions", UNSET)
        conditions: (
            list[InventoryFeatureSpatialCondition | InventoryGeometrySpatialCondition]
            | Unset
        ) = UNSET
        if _conditions is not UNSET:
            conditions = []
            for conditions_item_data in _conditions:

                def _parse_conditions_item(
                    data: object,
                ) -> (
                    InventoryFeatureSpatialCondition | InventoryGeometrySpatialCondition
                ):
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        conditions_item_type_0 = (
                            InventoryGeometrySpatialCondition.from_dict(data)
                        )

                        return conditions_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    conditions_item_type_1 = InventoryFeatureSpatialCondition.from_dict(
                        data
                    )

                    return conditions_item_type_1

                conditions_item = _parse_conditions_item(conditions_item_data)

                conditions.append(conditions_item)

        metric = cast(Literal["crown_spacing"] | Unset, d.pop("metric", UNSET))
        if metric != "crown_spacing" and not isinstance(metric, Unset):
            raise ValueError(f"metric must match const 'crown_spacing', got '{metric}'")

        _rank_by = d.pop("rank_by", UNSET)
        rank_by: InventoryCrownSpacingRank | Unset
        if isinstance(_rank_by, Unset):
            rank_by = UNSET
        else:
            rank_by = InventoryCrownSpacingRank(_rank_by)

        def _parse_max_crown_radius_source(
            data: object,
        ) -> (
            CanopyAllometryMaxCrownRadiusSource
            | InventoryColumnMaxCrownRadiusSource
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                max_crown_radius_source_type_0 = (
                    CanopyAllometryMaxCrownRadiusSource.from_dict(data)
                )

                return max_crown_radius_source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            max_crown_radius_source_type_1 = (
                InventoryColumnMaxCrownRadiusSource.from_dict(data)
            )

            return max_crown_radius_source_type_1

        max_crown_radius_source = _parse_max_crown_radius_source(
            d.pop("max_crown_radius_source", UNSET)
        )

        inventory_crown_spacing_treatment = cls(
            value=value,
            unit=unit,
            conditions=conditions,
            metric=metric,
            rank_by=rank_by,
            max_crown_radius_source=max_crown_radius_source,
        )

        inventory_crown_spacing_treatment.additional_properties = d
        return inventory_crown_spacing_treatment

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
