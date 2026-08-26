from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..models.canopy_horizontal_distribution import CanopyHorizontalDistribution
from ..models.canopy_species_inclusion import CanopySpeciesInclusion
from ..models.canopy_vertical_distribution import CanopyVerticalDistribution
from ..models.inventory_canopy_band import InventoryCanopyBand
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.allometry_canopy_biomass_source import AllometryCanopyBiomassSource
    from ..models.canopy_allometry_max_crown_radius_source import (
        CanopyAllometryMaxCrownRadiusSource,
    )
    from ..models.canopy_available_fuel import CanopyAvailableFuel
    from ..models.canopy_cbd_load_over_depth import CanopyCbdLoadOverDepth
    from ..models.canopy_cbd_running_mean import CanopyCbdRunningMean
    from ..models.canopy_cbh_mean import CanopyCbhMean
    from ..models.canopy_cbh_minimum import CanopyCbhMinimum
    from ..models.canopy_cbh_percentile import CanopyCbhPercentile
    from ..models.canopy_cc_cover_fraction import CanopyCcCoverFraction
    from ..models.canopy_cc_crown_overlap import CanopyCcCrownOverlap
    from ..models.canopy_cc_crown_union import CanopyCcCrownUnion
    from ..models.canopy_chm_height_percentile import CanopyChmHeightPercentile
    from ..models.canopy_fuelcalc_crown_class_adjustment import (
        CanopyFuelcalcCrownClassAdjustment,
    )
    from ..models.canopy_no_crown_class_adjustment import CanopyNoCrownClassAdjustment
    from ..models.canopy_profile_threshold import CanopyProfileThreshold
    from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
    from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
    from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
    from ..models.inventory_column_canopy_biomass_source import (
        InventoryColumnCanopyBiomassSource,
    )
    from ..models.inventory_column_max_crown_radius_source import (
        InventoryColumnMaxCrownRadiusSource,
    )


T = TypeVar("T", bound="CreateInventoryCanopyRequest")


@_attrs_define
class CreateInventoryCanopyRequest:
    """Request body for creating a canopy fuel grid from a tree inventory.

    Only live trees contribute canopy fuel: the worker reads live
    inventory records only, matching FuelCalc, which excludes dead trees
    from all calculations.

    Does not extend CreateGridRequestBase: like DUET and the 3D voxel
    grids, inventory-derived grids do not support modifications — apply
    treatments and modifications to the inventory before deriving canopy
    metrics.

        Attributes:
            source_inventory_id (str): ID of a completed tree inventory in this domain to derive canopy metrics from.
            biomass_source (AllometryCanopyBiomassSource | InventoryColumnCanopyBiomassSource | Unset): Where each tree's
                crown fuel mass comes from: allometric equations (default: NSVB) or an inventory column carrying precomputed
                available canopy fuel.
            available_fuel (CanopyAvailableFuel | None | Unset): How crown biomass reduces to available canopy fuel. Applies
                only with an allometry biomass source; resolved to `null` when the biomass source is an inventory column.
            species_inclusion (CanopySpeciesInclusion | Unset): Which species contribute canopy fuel to the profile.

                FuelCalc excludes most hardwoods from canopy fuel calculations by
                default; FastFuels includes every species unless told otherwise. With
                `fuelcalc_default`, the persisted source records the exclusion table
                the worker applied.
            crown_class_adjustment (CanopyFuelcalcCrownClassAdjustment | CanopyNoCrownClassAdjustment | Unset): Crown-weight
                adjustment for canopy position. `none` (default) applies no adjustment; `fuelcalc_table` applies the FuelCalc
                species x crown-class factors.
            min_tree_height (float | Unset): Trees shorter than this height in meters contribute no canopy fuel. Default 0.0
                includes every tree. FFE-FVS and the original FuelCalc method (RMRS-P-41) exclude trees under 1.83 m (6 ft) as
                surface fuel; FuelCalc 1.7 includes small trees down to 0.3 m via Brown's small-tree tables. Default: 0.0.
            vertical_distribution (CanopyVerticalDistribution | Unset): How each tree's available fuel is distributed from
                crown base to top.

                `reinhardt_2006` uses the species cumulative-fraction cubics fit from
                destructive sampling (Reinhardt et al. 2006, CJFR 36), applied through
                the published FuelCalc species crosswalk; species the crosswalk maps to
                no cubic (including all hardwoods) distribute uniformly. `uniform`
                spreads mass evenly over the crown for every tree — the FFE-FVS
                assumption.
            layer_depth (float | Unset): Vertical profile layer depth in meters. Default 0.3048 m (1 ft, the FuelCalc
                layer). Affects CBD smoothing and where threshold crossings land. Default: 0.3048.
            horizontal_distribution (CanopyHorizontalDistribution | Unset): How a tree's available fuel is attributed to
                output cells.

                `crown_projected` splits each tree's mass across the cells its
                projected crown overlaps, in proportion to the overlap area.
                `stem` assigns the whole mass to the cell containing the stem — the
                closest analogue to FuelCalc's plot computation.
            max_crown_radius_source (CanopyAllometryMaxCrownRadiusSource | InventoryColumnMaxCrownRadiusSource | Unset):
                Source of each tree's maximum crown radius, used by `crown_projected` attribution and the geometric canopy cover
                methods. Defaults to the `purves` allometry; set `{"type": "allometry", "equations": "crookston_stage"}` for the
                crown widths FuelCalc uses, or `{"type": "inventory_column", "column": ...}` to read a per-tree radius in meters
                (e.g. derived from LiDAR).
            cbd (CanopyCbdLoadOverDepth | CanopyCbdRunningMean | None | Unset): Canopy bulk density method. Defaults to the
                maximum 3.0 m running mean of the profile when the `cbd` band is requested.
            cbh (CanopyCbhMean | CanopyCbhMinimum | CanopyCbhPercentile | CanopyProfileThreshold | None | Unset): Canopy
                base height method. Defaults to the lowest profile-threshold crossing when the `cbh` band is requested.
            chm (CanopyChmHeightPercentile | CanopyProfileThreshold | None | Unset): Canopy height method. Defaults to the
                highest profile-threshold crossing when the `chm` band is requested.
            cc (CanopyCcCoverFraction | CanopyCcCrownOverlap | CanopyCcCrownUnion | None | Unset): Canopy cover method.
                Defaults to the geometric crown union when the `cc` band is requested.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            bands (list[InventoryCanopyBand] | Unset): Which output bands to produce. Defaults to the four LANDFIRE-parity
                canopy bands; add `cfl` for canopy fuel load.
            alignment (GridAlignmentDomainTarget | GridAlignmentGridTarget | GridAlignmentNativeTarget | Unset): Output
                lattice. Against the domain (`target: 'domain'`, the default) `resolution` defaults to 30 m — an inventory has
                no native cell size to inherit. Against another grid (`target: 'grid'`) omitting `resolution` matches that
                grid's lattice exactly. `target: 'native'` is not supported.
    """

    source_inventory_id: str
    biomass_source: (
        AllometryCanopyBiomassSource | InventoryColumnCanopyBiomassSource | Unset
    ) = UNSET
    available_fuel: CanopyAvailableFuel | None | Unset = UNSET
    species_inclusion: CanopySpeciesInclusion | Unset = UNSET
    crown_class_adjustment: (
        CanopyFuelcalcCrownClassAdjustment | CanopyNoCrownClassAdjustment | Unset
    ) = UNSET
    min_tree_height: float | Unset = 0.0
    vertical_distribution: CanopyVerticalDistribution | Unset = UNSET
    layer_depth: float | Unset = 0.3048
    horizontal_distribution: CanopyHorizontalDistribution | Unset = UNSET
    max_crown_radius_source: (
        CanopyAllometryMaxCrownRadiusSource
        | InventoryColumnMaxCrownRadiusSource
        | Unset
    ) = UNSET
    cbd: CanopyCbdLoadOverDepth | CanopyCbdRunningMean | None | Unset = UNSET
    cbh: (
        CanopyCbhMean
        | CanopyCbhMinimum
        | CanopyCbhPercentile
        | CanopyProfileThreshold
        | None
        | Unset
    ) = UNSET
    chm: CanopyChmHeightPercentile | CanopyProfileThreshold | None | Unset = UNSET
    cc: (
        CanopyCcCoverFraction | CanopyCcCrownOverlap | CanopyCcCrownUnion | None | Unset
    ) = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    bands: list[InventoryCanopyBand] | Unset = UNSET
    alignment: (
        GridAlignmentDomainTarget
        | GridAlignmentGridTarget
        | GridAlignmentNativeTarget
        | Unset
    ) = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.allometry_canopy_biomass_source import (
            AllometryCanopyBiomassSource,
        )
        from ..models.canopy_allometry_max_crown_radius_source import (
            CanopyAllometryMaxCrownRadiusSource,
        )
        from ..models.canopy_available_fuel import CanopyAvailableFuel
        from ..models.canopy_cbd_load_over_depth import CanopyCbdLoadOverDepth
        from ..models.canopy_cbd_running_mean import CanopyCbdRunningMean
        from ..models.canopy_cbh_mean import CanopyCbhMean
        from ..models.canopy_cbh_minimum import CanopyCbhMinimum
        from ..models.canopy_cbh_percentile import CanopyCbhPercentile
        from ..models.canopy_cc_cover_fraction import CanopyCcCoverFraction
        from ..models.canopy_cc_crown_overlap import CanopyCcCrownOverlap
        from ..models.canopy_cc_crown_union import CanopyCcCrownUnion
        from ..models.canopy_chm_height_percentile import CanopyChmHeightPercentile
        from ..models.canopy_no_crown_class_adjustment import (
            CanopyNoCrownClassAdjustment,
        )
        from ..models.canopy_profile_threshold import CanopyProfileThreshold
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget

        source_inventory_id = self.source_inventory_id

        biomass_source: dict[str, Any] | Unset
        if isinstance(self.biomass_source, Unset):
            biomass_source = UNSET
        elif isinstance(self.biomass_source, AllometryCanopyBiomassSource):
            biomass_source = self.biomass_source.to_dict()
        else:
            biomass_source = self.biomass_source.to_dict()

        available_fuel: dict[str, Any] | None | Unset
        if isinstance(self.available_fuel, Unset):
            available_fuel = UNSET
        elif isinstance(self.available_fuel, CanopyAvailableFuel):
            available_fuel = self.available_fuel.to_dict()
        else:
            available_fuel = self.available_fuel

        species_inclusion: str | Unset = UNSET
        if not isinstance(self.species_inclusion, Unset):
            species_inclusion = self.species_inclusion.value

        crown_class_adjustment: dict[str, Any] | Unset
        if isinstance(self.crown_class_adjustment, Unset):
            crown_class_adjustment = UNSET
        elif isinstance(self.crown_class_adjustment, CanopyNoCrownClassAdjustment):
            crown_class_adjustment = self.crown_class_adjustment.to_dict()
        else:
            crown_class_adjustment = self.crown_class_adjustment.to_dict()

        min_tree_height = self.min_tree_height

        vertical_distribution: str | Unset = UNSET
        if not isinstance(self.vertical_distribution, Unset):
            vertical_distribution = self.vertical_distribution.value

        layer_depth = self.layer_depth

        horizontal_distribution: str | Unset = UNSET
        if not isinstance(self.horizontal_distribution, Unset):
            horizontal_distribution = self.horizontal_distribution.value

        max_crown_radius_source: dict[str, Any] | Unset
        if isinstance(self.max_crown_radius_source, Unset):
            max_crown_radius_source = UNSET
        elif isinstance(
            self.max_crown_radius_source, CanopyAllometryMaxCrownRadiusSource
        ):
            max_crown_radius_source = self.max_crown_radius_source.to_dict()
        else:
            max_crown_radius_source = self.max_crown_radius_source.to_dict()

        cbd: dict[str, Any] | None | Unset
        if isinstance(self.cbd, Unset):
            cbd = UNSET
        elif isinstance(self.cbd, CanopyCbdRunningMean) or isinstance(
            self.cbd, CanopyCbdLoadOverDepth
        ):
            cbd = self.cbd.to_dict()
        else:
            cbd = self.cbd

        cbh: dict[str, Any] | None | Unset
        if isinstance(self.cbh, Unset):
            cbh = UNSET
        elif (
            isinstance(self.cbh, CanopyProfileThreshold)
            or isinstance(self.cbh, CanopyCbhMean)
            or isinstance(self.cbh, CanopyCbhPercentile)
            or isinstance(self.cbh, CanopyCbhMinimum)
        ):
            cbh = self.cbh.to_dict()
        else:
            cbh = self.cbh

        chm: dict[str, Any] | None | Unset
        if isinstance(self.chm, Unset):
            chm = UNSET
        elif isinstance(self.chm, CanopyProfileThreshold) or isinstance(
            self.chm, CanopyChmHeightPercentile
        ):
            chm = self.chm.to_dict()
        else:
            chm = self.chm

        cc: dict[str, Any] | None | Unset
        if isinstance(self.cc, Unset):
            cc = UNSET
        elif (
            isinstance(self.cc, CanopyCcCrownUnion)
            or isinstance(self.cc, CanopyCcCrownOverlap)
            or isinstance(self.cc, CanopyCcCoverFraction)
        ):
            cc = self.cc.to_dict()
        else:
            cc = self.cc

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        bands: list[str] | Unset = UNSET
        if not isinstance(self.bands, Unset):
            bands = []
            for bands_item_data in self.bands:
                bands_item = bands_item_data.value
                bands.append(bands_item)

        alignment: dict[str, Any] | Unset
        if isinstance(self.alignment, Unset):
            alignment = UNSET
        elif isinstance(self.alignment, GridAlignmentDomainTarget) or isinstance(
            self.alignment, GridAlignmentNativeTarget
        ):
            alignment = self.alignment.to_dict()
        else:
            alignment = self.alignment.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source_inventory_id": source_inventory_id,
            }
        )
        if biomass_source is not UNSET:
            field_dict["biomass_source"] = biomass_source
        if available_fuel is not UNSET:
            field_dict["available_fuel"] = available_fuel
        if species_inclusion is not UNSET:
            field_dict["species_inclusion"] = species_inclusion
        if crown_class_adjustment is not UNSET:
            field_dict["crown_class_adjustment"] = crown_class_adjustment
        if min_tree_height is not UNSET:
            field_dict["min_tree_height"] = min_tree_height
        if vertical_distribution is not UNSET:
            field_dict["vertical_distribution"] = vertical_distribution
        if layer_depth is not UNSET:
            field_dict["layer_depth"] = layer_depth
        if horizontal_distribution is not UNSET:
            field_dict["horizontal_distribution"] = horizontal_distribution
        if max_crown_radius_source is not UNSET:
            field_dict["max_crown_radius_source"] = max_crown_radius_source
        if cbd is not UNSET:
            field_dict["cbd"] = cbd
        if cbh is not UNSET:
            field_dict["cbh"] = cbh
        if chm is not UNSET:
            field_dict["chm"] = chm
        if cc is not UNSET:
            field_dict["cc"] = cc
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if bands is not UNSET:
            field_dict["bands"] = bands
        if alignment is not UNSET:
            field_dict["alignment"] = alignment

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.allometry_canopy_biomass_source import (
            AllometryCanopyBiomassSource,
        )
        from ..models.canopy_allometry_max_crown_radius_source import (
            CanopyAllometryMaxCrownRadiusSource,
        )
        from ..models.canopy_available_fuel import CanopyAvailableFuel
        from ..models.canopy_cbd_load_over_depth import CanopyCbdLoadOverDepth
        from ..models.canopy_cbd_running_mean import CanopyCbdRunningMean
        from ..models.canopy_cbh_mean import CanopyCbhMean
        from ..models.canopy_cbh_minimum import CanopyCbhMinimum
        from ..models.canopy_cbh_percentile import CanopyCbhPercentile
        from ..models.canopy_cc_cover_fraction import CanopyCcCoverFraction
        from ..models.canopy_cc_crown_overlap import CanopyCcCrownOverlap
        from ..models.canopy_cc_crown_union import CanopyCcCrownUnion
        from ..models.canopy_chm_height_percentile import CanopyChmHeightPercentile
        from ..models.canopy_fuelcalc_crown_class_adjustment import (
            CanopyFuelcalcCrownClassAdjustment,
        )
        from ..models.canopy_no_crown_class_adjustment import (
            CanopyNoCrownClassAdjustment,
        )
        from ..models.canopy_profile_threshold import CanopyProfileThreshold
        from ..models.grid_alignment_domain_target import GridAlignmentDomainTarget
        from ..models.grid_alignment_grid_target import GridAlignmentGridTarget
        from ..models.grid_alignment_native_target import GridAlignmentNativeTarget
        from ..models.inventory_column_canopy_biomass_source import (
            InventoryColumnCanopyBiomassSource,
        )
        from ..models.inventory_column_max_crown_radius_source import (
            InventoryColumnMaxCrownRadiusSource,
        )

        d = dict(src_dict)
        source_inventory_id = d.pop("source_inventory_id")

        def _parse_biomass_source(
            data: object,
        ) -> AllometryCanopyBiomassSource | InventoryColumnCanopyBiomassSource | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                biomass_source_type_0 = AllometryCanopyBiomassSource.from_dict(data)

                return biomass_source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            biomass_source_type_1 = InventoryColumnCanopyBiomassSource.from_dict(data)

            return biomass_source_type_1

        biomass_source = _parse_biomass_source(d.pop("biomass_source", UNSET))

        def _parse_available_fuel(data: object) -> CanopyAvailableFuel | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                available_fuel_type_0 = CanopyAvailableFuel.from_dict(data)

                return available_fuel_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CanopyAvailableFuel | None | Unset, data)

        available_fuel = _parse_available_fuel(d.pop("available_fuel", UNSET))

        _species_inclusion = d.pop("species_inclusion", UNSET)
        species_inclusion: CanopySpeciesInclusion | Unset
        if isinstance(_species_inclusion, Unset):
            species_inclusion = UNSET
        else:
            species_inclusion = CanopySpeciesInclusion(_species_inclusion)

        def _parse_crown_class_adjustment(
            data: object,
        ) -> CanopyFuelcalcCrownClassAdjustment | CanopyNoCrownClassAdjustment | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_class_adjustment_type_0 = CanopyNoCrownClassAdjustment.from_dict(
                    data
                )

                return crown_class_adjustment_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            crown_class_adjustment_type_1 = (
                CanopyFuelcalcCrownClassAdjustment.from_dict(data)
            )

            return crown_class_adjustment_type_1

        crown_class_adjustment = _parse_crown_class_adjustment(
            d.pop("crown_class_adjustment", UNSET)
        )

        min_tree_height = d.pop("min_tree_height", UNSET)

        _vertical_distribution = d.pop("vertical_distribution", UNSET)
        vertical_distribution: CanopyVerticalDistribution | Unset
        if isinstance(_vertical_distribution, Unset):
            vertical_distribution = UNSET
        else:
            vertical_distribution = CanopyVerticalDistribution(_vertical_distribution)

        layer_depth = d.pop("layer_depth", UNSET)

        _horizontal_distribution = d.pop("horizontal_distribution", UNSET)
        horizontal_distribution: CanopyHorizontalDistribution | Unset
        if isinstance(_horizontal_distribution, Unset):
            horizontal_distribution = UNSET
        else:
            horizontal_distribution = CanopyHorizontalDistribution(
                _horizontal_distribution
            )

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

        def _parse_cbd(
            data: object,
        ) -> CanopyCbdLoadOverDepth | CanopyCbdRunningMean | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cbd_type_0_type_0 = CanopyCbdRunningMean.from_dict(data)

                return cbd_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cbd_type_0_type_1 = CanopyCbdLoadOverDepth.from_dict(data)

                return cbd_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CanopyCbdLoadOverDepth | CanopyCbdRunningMean | None | Unset, data
            )

        cbd = _parse_cbd(d.pop("cbd", UNSET))

        def _parse_cbh(
            data: object,
        ) -> (
            CanopyCbhMean
            | CanopyCbhMinimum
            | CanopyCbhPercentile
            | CanopyProfileThreshold
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cbh_type_0_type_0 = CanopyProfileThreshold.from_dict(data)

                return cbh_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cbh_type_0_type_1 = CanopyCbhMean.from_dict(data)

                return cbh_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cbh_type_0_type_2 = CanopyCbhPercentile.from_dict(data)

                return cbh_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cbh_type_0_type_3 = CanopyCbhMinimum.from_dict(data)

                return cbh_type_0_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CanopyCbhMean
                | CanopyCbhMinimum
                | CanopyCbhPercentile
                | CanopyProfileThreshold
                | None
                | Unset,
                data,
            )

        cbh = _parse_cbh(d.pop("cbh", UNSET))

        def _parse_chm(
            data: object,
        ) -> CanopyChmHeightPercentile | CanopyProfileThreshold | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chm_type_0_type_0 = CanopyProfileThreshold.from_dict(data)

                return chm_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chm_type_0_type_1 = CanopyChmHeightPercentile.from_dict(data)

                return chm_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CanopyChmHeightPercentile | CanopyProfileThreshold | None | Unset, data
            )

        chm = _parse_chm(d.pop("chm", UNSET))

        def _parse_cc(
            data: object,
        ) -> (
            CanopyCcCoverFraction
            | CanopyCcCrownOverlap
            | CanopyCcCrownUnion
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cc_type_0_type_0 = CanopyCcCrownUnion.from_dict(data)

                return cc_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cc_type_0_type_1 = CanopyCcCrownOverlap.from_dict(data)

                return cc_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                cc_type_0_type_2 = CanopyCcCoverFraction.from_dict(data)

                return cc_type_0_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CanopyCcCoverFraction
                | CanopyCcCrownOverlap
                | CanopyCcCrownUnion
                | None
                | Unset,
                data,
            )

        cc = _parse_cc(d.pop("cc", UNSET))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _bands = d.pop("bands", UNSET)
        bands: list[InventoryCanopyBand] | Unset = UNSET
        if _bands is not UNSET:
            bands = []
            for bands_item_data in _bands:
                bands_item = InventoryCanopyBand(bands_item_data)

                bands.append(bands_item)

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

        create_inventory_canopy_request = cls(
            source_inventory_id=source_inventory_id,
            biomass_source=biomass_source,
            available_fuel=available_fuel,
            species_inclusion=species_inclusion,
            crown_class_adjustment=crown_class_adjustment,
            min_tree_height=min_tree_height,
            vertical_distribution=vertical_distribution,
            layer_depth=layer_depth,
            horizontal_distribution=horizontal_distribution,
            max_crown_radius_source=max_crown_radius_source,
            cbd=cbd,
            cbh=cbh,
            chm=chm,
            cc=cc,
            name=name,
            description=description,
            tags=tags,
            bands=bands,
            alignment=alignment,
        )

        return create_inventory_canopy_request
