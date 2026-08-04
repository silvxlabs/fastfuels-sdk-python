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

from ..models.inventory_diameter_treatment_method import (
    InventoryDiameterTreatmentMethod,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inventory_feature_spatial_condition import (
        InventoryFeatureSpatialCondition,
    )
    from ..models.inventory_geometry_spatial_condition import (
        InventoryGeometrySpatialCondition,
    )


T = TypeVar("T", bound="InventoryDiameterTreatment")


@_attrs_define
class InventoryDiameterTreatment:
    """Thin to a diameter-at-breast-height limit.

    A hard cutoff: ``from_below`` removes trees smaller than ``value``,
    ``from_above`` removes trees larger than ``value``. ``proportional`` does not
    apply to a diameter limit and is not an option here.

        Attributes:
            method (InventoryDiameterTreatmentMethod): `from_below` removes trees below the limit; `from_above` removes
                trees above the limit.
            value (float): Diameter-at-breast-height limit, in cm unless `unit` is set.
            unit (None | str | Unset): Optional unit for `value`. Must be canonical and dimensionally compatible with the
                metric's native unit; converted before the treatment is applied.
            conditions (list[InventoryFeatureSpatialCondition | InventoryGeometrySpatialCondition] | Unset): Spatial
                conditions restricting the treatment to a region (within/outside/intersects a geometry or Feature). An empty
                list applies the treatment to the entire inventory.
            metric (Literal['diameter'] | Unset):  Default: 'diameter'.
    """

    method: InventoryDiameterTreatmentMethod
    value: float
    unit: None | str | Unset = UNSET
    conditions: (
        list[InventoryFeatureSpatialCondition | InventoryGeometrySpatialCondition]
        | Unset
    ) = UNSET
    metric: Literal["diameter"] | Unset = "diameter"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_geometry_spatial_condition import (
            InventoryGeometrySpatialCondition,
        )

        method = self.method.value

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method": method,
                "value": value,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if metric is not UNSET:
            field_dict["metric"] = metric

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory_feature_spatial_condition import (
            InventoryFeatureSpatialCondition,
        )
        from ..models.inventory_geometry_spatial_condition import (
            InventoryGeometrySpatialCondition,
        )

        d = dict(src_dict)
        method = InventoryDiameterTreatmentMethod(d.pop("method"))

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

        metric = cast(Literal["diameter"] | Unset, d.pop("metric", UNSET))
        if metric != "diameter" and not isinstance(metric, Unset):
            raise ValueError(f"metric must match const 'diameter', got '{metric}'")

        inventory_diameter_treatment = cls(
            method=method,
            value=value,
            unit=unit,
            conditions=conditions,
            metric=metric,
        )

        inventory_diameter_treatment.additional_properties = d
        return inventory_diameter_treatment

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
