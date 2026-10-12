from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..models.crown_profile_model import CrownProfileModel
from ..models.tree_band import TreeBand
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allometry_biomass_source import AllometryBiomassSource
    from ..models.allometry_max_crown_radius_source import AllometryMaxCrownRadiusSource
    from ..models.crown_feature_crown_geometry_source import (
        CrownFeatureCrownGeometrySource,
    )
    from ..models.inventory_column_max_crown_radius_source import (
        InventoryColumnMaxCrownRadiusSource,
    )
    from ..models.inventory_columns_biomass_source import InventoryColumnsBiomassSource
    from ..models.moisture_model import MoistureModel
    from ..models.parametric_crown_geometry_source import ParametricCrownGeometrySource
    from ..models.resolution_3d import Resolution3D


T = TypeVar("T", bound="CreateTreeInventoryRequest")


@_attrs_define
class CreateTreeInventoryRequest:
    """Request body for creating a tree fuel grid from a tree inventory.

    Does not extend CreateGridRequestBase because 3D grids do not support
    modifications — modifications must be applied to the inventory before
    voxelization, not to the resulting voxel grid.

        Attributes:
            source_inventory_id (str): ID of a completed tree inventory to voxelize.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            resolution (Resolution3D | Unset): Voxel resolution for a 3D grid.

                `horizontal` applies to both x and y (fastfuels-core requires isotropic
                horizontal resolution). `vertical` is independent.
            bands (list[TreeBand] | Unset): Which output bands to produce. Defaults to `bulk_density.foliage.live`.
            crown_profile_model (CrownProfileModel | Unset): Crown geometry models — which voxels a tree's crown occupies.
            biomass_source (AllometryBiomassSource | InventoryColumnsBiomassSource | Unset): Biomass source and requested
                biomass components.
            max_crown_radius_source (AllometryMaxCrownRadiusSource | InventoryColumnMaxCrownRadiusSource | Unset): Source of
                each tree's maximum crown radius. `{"type": "allometry"}` (default): the Purves et al. (2007) maximum crown
                radius for `purves`, `cone`, `cylinder`, and the ellipsoid and paraboloid shapes, so a tree's crown is equally
                wide under each of them and only the shape changes; `beta` uses its own allometric radius. `{"type":
                "inventory_column", "column": ...}`: read a per-tree maximum crown radius (m) from an inventory column (e.g.
                derived from LiDAR); `crown_profile_model` still sets the crown shape.
            crown_geometry_source (CrownFeatureCrownGeometrySource | ParametricCrownGeometrySource | Unset): Where crown
                shapes come from. `{"type": "parametric"}` (default): every crown is drawn from `crown_profile_model` and
                `max_crown_radius_source`. `{"type": "crown_feature", "feature_id": ...}`: a tree with a crown in the crown
                Feature, matched by `tree_id`, gets a measured crown. Its outline is the crown's CHM cells, its top is each
                cell's CHM height, and its bottom follows `crown_profile_model` up from the crown base, at least one voxel below
                the top but never below the crown base. `max_crown_radius_source` does not apply to measured crowns. A tree with
                no crown in the Feature, whose crown does not contain its stem, or with no CHM height above its crown base, is
                drawn parametrically. Crowns of trees not in the inventory are ignored. Every tree keeps the mass
                `biomass_source` gives it. Requires an inventory with a `tree_id` column.
            max_bulk_density (float | None | Unset): Upper limit on bulk density, in kg/m**3. In any voxel where a biomass
                component's bulk density, live and dead combined, exceeds the limit, that component's live and dead bulk density
                are scaled down to it, keeping their live/dead split, and `leaf_area_density` is scaled with foliage. Fuel above
                the limit is removed from the grid. Omit for no limit.
            moisture_model (MoistureModel | None | Unset): Live/dead fuel moisture model. Applied only when matching
                fuel_moisture bands are requested. Live defaults to uniform 100.0; dead defaults to uniform 10.0.
            seed (int | Unset): Random seed for reproducibility. Controls stochastic tree voxel sampling and biomass
                distribution. Generated randomly if omitted; persisted on the grid document either way so re-running a grid
                always yields bit-identical output.
    """

    source_inventory_id: str
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    resolution: Resolution3D | Unset = UNSET
    bands: list[TreeBand] | Unset = UNSET
    crown_profile_model: CrownProfileModel | Unset = UNSET
    biomass_source: AllometryBiomassSource | InventoryColumnsBiomassSource | Unset = (
        UNSET
    )
    max_crown_radius_source: (
        AllometryMaxCrownRadiusSource | InventoryColumnMaxCrownRadiusSource | Unset
    ) = UNSET
    crown_geometry_source: (
        CrownFeatureCrownGeometrySource | ParametricCrownGeometrySource | Unset
    ) = UNSET
    max_bulk_density: float | None | Unset = UNSET
    moisture_model: MoistureModel | None | Unset = UNSET
    seed: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.allometry_biomass_source import AllometryBiomassSource
        from ..models.allometry_max_crown_radius_source import (
            AllometryMaxCrownRadiusSource,
        )
        from ..models.moisture_model import MoistureModel
        from ..models.parametric_crown_geometry_source import (
            ParametricCrownGeometrySource,
        )

        source_inventory_id = self.source_inventory_id

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        resolution: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resolution, Unset):
            resolution = self.resolution.to_dict()

        bands: list[str] | Unset = UNSET
        if not isinstance(self.bands, Unset):
            bands = []
            for bands_item_data in self.bands:
                bands_item = bands_item_data.value
                bands.append(bands_item)

        crown_profile_model: str | Unset = UNSET
        if not isinstance(self.crown_profile_model, Unset):
            crown_profile_model = self.crown_profile_model.value

        biomass_source: dict[str, Any] | Unset
        if isinstance(self.biomass_source, Unset):
            biomass_source = UNSET
        elif isinstance(self.biomass_source, AllometryBiomassSource):
            biomass_source = self.biomass_source.to_dict()
        else:
            biomass_source = self.biomass_source.to_dict()

        max_crown_radius_source: dict[str, Any] | Unset
        if isinstance(self.max_crown_radius_source, Unset):
            max_crown_radius_source = UNSET
        elif isinstance(self.max_crown_radius_source, AllometryMaxCrownRadiusSource):
            max_crown_radius_source = self.max_crown_radius_source.to_dict()
        else:
            max_crown_radius_source = self.max_crown_radius_source.to_dict()

        crown_geometry_source: dict[str, Any] | Unset
        if isinstance(self.crown_geometry_source, Unset):
            crown_geometry_source = UNSET
        elif isinstance(self.crown_geometry_source, ParametricCrownGeometrySource):
            crown_geometry_source = self.crown_geometry_source.to_dict()
        else:
            crown_geometry_source = self.crown_geometry_source.to_dict()

        max_bulk_density: float | None | Unset
        if isinstance(self.max_bulk_density, Unset):
            max_bulk_density = UNSET
        else:
            max_bulk_density = self.max_bulk_density

        moisture_model: dict[str, Any] | None | Unset
        if isinstance(self.moisture_model, Unset):
            moisture_model = UNSET
        elif isinstance(self.moisture_model, MoistureModel):
            moisture_model = self.moisture_model.to_dict()
        else:
            moisture_model = self.moisture_model

        seed = self.seed

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source_inventory_id": source_inventory_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if resolution is not UNSET:
            field_dict["resolution"] = resolution
        if bands is not UNSET:
            field_dict["bands"] = bands
        if crown_profile_model is not UNSET:
            field_dict["crown_profile_model"] = crown_profile_model
        if biomass_source is not UNSET:
            field_dict["biomass_source"] = biomass_source
        if max_crown_radius_source is not UNSET:
            field_dict["max_crown_radius_source"] = max_crown_radius_source
        if crown_geometry_source is not UNSET:
            field_dict["crown_geometry_source"] = crown_geometry_source
        if max_bulk_density is not UNSET:
            field_dict["max_bulk_density"] = max_bulk_density
        if moisture_model is not UNSET:
            field_dict["moisture_model"] = moisture_model
        if seed is not UNSET:
            field_dict["seed"] = seed

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.allometry_biomass_source import AllometryBiomassSource
        from ..models.allometry_max_crown_radius_source import (
            AllometryMaxCrownRadiusSource,
        )
        from ..models.crown_feature_crown_geometry_source import (
            CrownFeatureCrownGeometrySource,
        )
        from ..models.inventory_column_max_crown_radius_source import (
            InventoryColumnMaxCrownRadiusSource,
        )
        from ..models.inventory_columns_biomass_source import (
            InventoryColumnsBiomassSource,
        )
        from ..models.moisture_model import MoistureModel
        from ..models.parametric_crown_geometry_source import (
            ParametricCrownGeometrySource,
        )
        from ..models.resolution_3d import Resolution3D

        d = dict(src_dict)
        source_inventory_id = d.pop("source_inventory_id")

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _resolution = d.pop("resolution", UNSET)
        resolution: Resolution3D | Unset
        if isinstance(_resolution, Unset):
            resolution = UNSET
        else:
            resolution = Resolution3D.from_dict(_resolution)

        _bands = d.pop("bands", UNSET)
        bands: list[TreeBand] | Unset = UNSET
        if _bands is not UNSET:
            bands = []
            for bands_item_data in _bands:
                bands_item = TreeBand(bands_item_data)

                bands.append(bands_item)

        _crown_profile_model = d.pop("crown_profile_model", UNSET)
        crown_profile_model: CrownProfileModel | Unset
        if isinstance(_crown_profile_model, Unset):
            crown_profile_model = UNSET
        else:
            crown_profile_model = CrownProfileModel(_crown_profile_model)

        def _parse_biomass_source(
            data: object,
        ) -> AllometryBiomassSource | InventoryColumnsBiomassSource | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                biomass_source_type_0 = AllometryBiomassSource.from_dict(data)

                return biomass_source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            biomass_source_type_1 = InventoryColumnsBiomassSource.from_dict(data)

            return biomass_source_type_1

        biomass_source = _parse_biomass_source(d.pop("biomass_source", UNSET))

        def _parse_max_crown_radius_source(
            data: object,
        ) -> (
            AllometryMaxCrownRadiusSource | InventoryColumnMaxCrownRadiusSource | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                max_crown_radius_source_type_0 = (
                    AllometryMaxCrownRadiusSource.from_dict(data)
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

        def _parse_crown_geometry_source(
            data: object,
        ) -> CrownFeatureCrownGeometrySource | ParametricCrownGeometrySource | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_geometry_source_type_0 = ParametricCrownGeometrySource.from_dict(
                    data
                )

                return crown_geometry_source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            crown_geometry_source_type_1 = CrownFeatureCrownGeometrySource.from_dict(
                data
            )

            return crown_geometry_source_type_1

        crown_geometry_source = _parse_crown_geometry_source(
            d.pop("crown_geometry_source", UNSET)
        )

        def _parse_max_bulk_density(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_bulk_density = _parse_max_bulk_density(d.pop("max_bulk_density", UNSET))

        def _parse_moisture_model(data: object) -> MoistureModel | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                moisture_model_type_0 = MoistureModel.from_dict(data)

                return moisture_model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MoistureModel | None | Unset, data)

        moisture_model = _parse_moisture_model(d.pop("moisture_model", UNSET))

        seed = d.pop("seed", UNSET)

        create_tree_inventory_request = cls(
            source_inventory_id=source_inventory_id,
            name=name,
            description=description,
            tags=tags,
            resolution=resolution,
            bands=bands,
            crown_profile_model=crown_profile_model,
            biomass_source=biomass_source,
            max_crown_radius_source=max_crown_radius_source,
            crown_geometry_source=crown_geometry_source,
            max_bulk_density=max_bulk_density,
            moisture_model=moisture_model,
            seed=seed,
        )

        return create_tree_inventory_request
