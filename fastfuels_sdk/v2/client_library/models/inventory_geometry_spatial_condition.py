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

from ..models.spatial_operator import SpatialOperator
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inventory_geometry_spatial_condition_crs_type_0 import (
        InventoryGeometrySpatialConditionCrsType0,
    )
    from ..models.inventory_geometry_spatial_condition_geometry import (
        InventoryGeometrySpatialConditionGeometry,
    )


T = TypeVar("T", bound="InventoryGeometrySpatialCondition")


@_attrs_define
class InventoryGeometrySpatialCondition:
    """Spatial condition that tests tree locations against an inline GeoJSON
    geometry.

    Trees are points, so the test is always point-in-(optionally-buffered)-geometry.
    Use this variant when the geometry is supplied directly in the request; for a
    persisted geometry hosted as a Feature resource, use
    ``InventoryFeatureSpatialCondition``.

        Attributes:
            source (Literal['geometry']): Discriminator selecting this variant. Must be the literal string `"geometry"`. Use
                `"feature"` instead to reference a persisted Feature resource by id.
            operator (SpatialOperator): Spatial relationship operators for geometry-based conditions.

                - within: Select items whose target (centroid or cell) is inside the geometry
                - outside: Select items whose target is outside the geometry (inverse of within)
                - intersects: Select items whose target overlaps with the geometry
            geometry (InventoryGeometrySpatialConditionGeometry): Inline GeoJSON geometry. Polygon and MultiPolygon are the
                common shapes; LineString geometries should typically be paired with a non-zero `buffer_m` since a tree point
                almost never lies exactly on a line.
            crs (InventoryGeometrySpatialConditionCrsType0 | None | Unset): CRS of `geometry`, expressed as a GeoJSON CRS
                object (`{"type": "name", "properties": {"name": "EPSG:..."}}`). Defaults to the domain CRS when null.
            buffer_m (float | None | Unset): Optional buffer distance in meters applied to the geometry (in the domain's
                projected CRS) before testing. Use a non-zero buffer to widen the masked region beyond the literal geometry.
    """

    source: Literal["geometry"]
    operator: SpatialOperator
    geometry: InventoryGeometrySpatialConditionGeometry
    crs: InventoryGeometrySpatialConditionCrsType0 | None | Unset = UNSET
    buffer_m: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_geometry_spatial_condition_crs_type_0 import (
            InventoryGeometrySpatialConditionCrsType0,
        )

        source = self.source

        operator = self.operator.value

        geometry = self.geometry.to_dict()

        crs: dict[str, Any] | None | Unset
        if isinstance(self.crs, Unset):
            crs = UNSET
        elif isinstance(self.crs, InventoryGeometrySpatialConditionCrsType0):
            crs = self.crs.to_dict()
        else:
            crs = self.crs

        buffer_m: float | None | Unset
        if isinstance(self.buffer_m, Unset):
            buffer_m = UNSET
        else:
            buffer_m = self.buffer_m

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "operator": operator,
                "geometry": geometry,
            }
        )
        if crs is not UNSET:
            field_dict["crs"] = crs
        if buffer_m is not UNSET:
            field_dict["buffer_m"] = buffer_m

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory_geometry_spatial_condition_crs_type_0 import (
            InventoryGeometrySpatialConditionCrsType0,
        )
        from ..models.inventory_geometry_spatial_condition_geometry import (
            InventoryGeometrySpatialConditionGeometry,
        )

        d = dict(src_dict)
        source = cast(Literal["geometry"], d.pop("source"))
        if source != "geometry":
            raise ValueError(f"source must match const 'geometry', got '{source}'")

        operator = SpatialOperator(d.pop("operator"))

        geometry = InventoryGeometrySpatialConditionGeometry.from_dict(
            d.pop("geometry")
        )

        def _parse_crs(
            data: object,
        ) -> InventoryGeometrySpatialConditionCrsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crs_type_0 = InventoryGeometrySpatialConditionCrsType0.from_dict(data)

                return crs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InventoryGeometrySpatialConditionCrsType0 | None | Unset, data)

        crs = _parse_crs(d.pop("crs", UNSET))

        def _parse_buffer_m(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        buffer_m = _parse_buffer_m(d.pop("buffer_m", UNSET))

        inventory_geometry_spatial_condition = cls(
            source=source,
            operator=operator,
            geometry=geometry,
            crs=crs,
            buffer_m=buffer_m,
        )

        inventory_geometry_spatial_condition.additional_properties = d
        return inventory_geometry_spatial_condition

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
