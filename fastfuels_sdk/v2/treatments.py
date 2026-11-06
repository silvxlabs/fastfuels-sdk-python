"""
fastfuels_sdk/v2/treatments.py

Treatment primitives for tree inventories.

A treatment thins a tree inventory by removing stems until the stand reaches a
target — a residual basal area, a diameter limit, or a minimum spacing between
crowns. Pass treatments to a
tree-inventory creator's ``treatments=`` argument, or to
:meth:`fastfuels_sdk.v2.inventories.Inventory.apply_treatments` on an inventory
you already hold. These builders construct the generated treatment models so
callers don't have to.

The optional ``conditions`` argument restricts a treatment to a subarea
(``InventoryFeatureSpatialCondition`` / ``InventoryGeometrySpatialCondition``);
it is passed through as-is — there is no condition-builder vocabulary yet.
"""

from typing import Optional

from fastfuels_sdk.v2.client_library.models import (
    CanopyAllometryMaxCrownRadiusSource,
    CanopyCrownWidthEquations,
    InventoryBasalAreaTreatment,
    InventoryColumnMaxCrownRadiusSource,
    InventoryCrownSpacingRank,
    InventoryCrownSpacingTreatment,
    InventoryDiameterTreatment,
    InventoryDiameterTreatmentMethod,
    InventoryTreatmentMethod,
)
from fastfuels_sdk.v2.client_library.types import UNSET

__all__ = ["basal_area_treatment", "diameter_treatment", "crown_spacing_treatment"]


def basal_area_treatment(
    method: str,
    value: float,
    *,
    unit: Optional[str] = None,
    conditions: Optional[list] = None,
) -> InventoryBasalAreaTreatment:
    """Build a treatment that thins an inventory to a residual basal area.

    Parameters
    ----------
    method : {"from_below", "from_above", "proportional"}
        How stems are removed: "from_below" removes the smallest trees first,
        "from_above" the largest first, "proportional" removes across all size
        classes. An ``InventoryTreatmentMethod`` member is also accepted.
    value : float
        The residual basal area to thin to (default unit m**2/ha).
    unit : str, optional
        Unit of ``value`` if not the default.
    conditions : list, optional
        Spatial conditions restricting the treatment to a subarea
        (``InventoryFeatureSpatialCondition`` / ``InventoryGeometrySpatialCondition``).

    Returns
    -------
    InventoryBasalAreaTreatment
        A treatment for a creator's ``treatments=`` list or
        :meth:`Inventory.apply_treatments`.

    Examples
    --------
    Thin from below to a residual basal area of 25 m**2/ha:

    >>> import fastfuels_sdk.v2 as ff
    >>> inventory.apply_treatments([ff.basal_area_treatment("from_below", 25.0)])
    """
    return InventoryBasalAreaTreatment(
        method=_basal_area_method(method),
        value=value,
        unit=unit if unit is not None else UNSET,
        conditions=list(conditions) if conditions is not None else UNSET,
    )


def diameter_treatment(
    method: str,
    value: float,
    *,
    unit: Optional[str] = None,
    conditions: Optional[list] = None,
) -> InventoryDiameterTreatment:
    """Build a treatment that thins an inventory to a diameter limit.

    Parameters
    ----------
    method : {"from_below", "from_above"}
        "from_below" removes trees smaller than ``value`` (clears suppressed
        understory stems); "from_above" removes those larger than ``value``. An
        ``InventoryDiameterTreatmentMethod`` member is also accepted.
    value : float
        The diameter limit (default unit cm dbh).
    unit : str, optional
        Unit of ``value`` if not the default.
    conditions : list, optional
        Spatial conditions restricting the treatment to a subarea
        (``InventoryFeatureSpatialCondition`` / ``InventoryGeometrySpatialCondition``).

    Returns
    -------
    InventoryDiameterTreatment
        A treatment for a creator's ``treatments=`` list or
        :meth:`Inventory.apply_treatments`.

    Examples
    --------
    Remove trees smaller than 10 cm dbh:

    >>> import fastfuels_sdk.v2 as ff
    >>> inventory.apply_treatments([ff.diameter_treatment("from_below", 10.0)])
    """
    return InventoryDiameterTreatment(
        method=_diameter_method(method),
        value=value,
        unit=unit if unit is not None else UNSET,
        conditions=list(conditions) if conditions is not None else UNSET,
    )


def crown_spacing_treatment(
    value: float,
    *,
    unit: Optional[str] = None,
    rank_by: Optional[str] = None,
    max_crown_radius_equations: Optional[str] = None,
    max_crown_radius_column: Optional[str] = None,
    conditions: Optional[list] = None,
) -> InventoryCrownSpacingTreatment:
    """Build a treatment that thins an inventory to a minimum crown spacing.

    Trees are visited from the largest ``rank_by`` value down, and each is
    kept only if its crown clears every crown already kept by at least
    ``value``, crown edge to crown edge.

    Parameters
    ----------
    value : float
        The minimum gap between retained crowns (default unit m).
    unit : str, optional
        Unit of ``value`` if not the default, e.g. "ft".
    rank_by : {"dbh", "height"}, optional
        Which tree is kept when two crowns are too close: "dbh" (the default)
        keeps the larger diameter, "height" the taller tree. An
        ``InventoryCrownSpacingRank`` member is also accepted.
    max_crown_radius_equations : {"purves", "crookston_stage"}, optional
        Allometric equations for each tree's crown radius: "purves" (the
        default) or "crookston_stage". Mutually exclusive with
        ``max_crown_radius_column``.
    max_crown_radius_column : str, optional
        Inventory column holding each tree's crown radius in meters, e.g.
        "crown_radius", used in place of allometry. Trees with no value in
        the column use their "purves" radius. Mutually exclusive with
        ``max_crown_radius_equations``.
    conditions : list, optional
        Spatial conditions restricting the treatment to a subarea
        (``InventoryFeatureSpatialCondition`` / ``InventoryGeometrySpatialCondition``).
        Only trees whose stem is in the subarea are removed; they must also
        clear the crowns of nearby trees outside it.

    Returns
    -------
    InventoryCrownSpacingTreatment
        A treatment for a creator's ``treatments=`` list or
        :meth:`Inventory.apply_treatments`.

    Raises
    ------
    ValueError
        If ``rank_by`` or ``max_crown_radius_equations`` is not a recognized
        value, or both ``max_crown_radius_equations`` and
        ``max_crown_radius_column`` are given.

    Examples
    --------
    Thin to at least 3 m between crowns, keeping the larger-diameter trees:

    >>> import fastfuels_sdk.v2 as ff
    >>> inventory.apply_treatments([ff.crown_spacing_treatment(3.0)])

    Thin a CHM inventory with crown segmentation, keeping the taller trees
    and reading the measured ``crown_radius`` column:

    >>> ff.crown_spacing_treatment(
    ...     3.0, rank_by="height", max_crown_radius_column="crown_radius"
    ... )
    """
    return InventoryCrownSpacingTreatment(
        value=value,
        unit=unit if unit is not None else UNSET,
        rank_by=_crown_spacing_rank(rank_by) if rank_by is not None else UNSET,
        max_crown_radius_source=_max_crown_radius_source(
            max_crown_radius_equations, max_crown_radius_column
        ),
        conditions=list(conditions) if conditions is not None else UNSET,
    )


def _basal_area_method(method) -> InventoryTreatmentMethod:
    """Coerce a string or enum member to an ``InventoryTreatmentMethod``."""
    if isinstance(method, InventoryTreatmentMethod):
        return method
    return InventoryTreatmentMethod(method)


def _diameter_method(method) -> InventoryDiameterTreatmentMethod:
    """Coerce a string or enum member to an ``InventoryDiameterTreatmentMethod``."""
    if isinstance(method, InventoryDiameterTreatmentMethod):
        return method
    return InventoryDiameterTreatmentMethod(method)


def _crown_spacing_rank(rank_by) -> InventoryCrownSpacingRank:
    """Coerce a string or enum member to an ``InventoryCrownSpacingRank``."""
    if isinstance(rank_by, InventoryCrownSpacingRank):
        return rank_by
    return InventoryCrownSpacingRank(rank_by)


def _max_crown_radius_source(equations, column):
    """Build the max-crown-radius source union from friendly kwargs, or UNSET."""
    if equations is not None and column is not None:
        raise ValueError(
            "Specify at most one of max_crown_radius_equations or "
            "max_crown_radius_column."
        )
    if column is not None:
        return InventoryColumnMaxCrownRadiusSource(column=column)
    if equations is not None:
        return CanopyAllometryMaxCrownRadiusSource(
            equations=CanopyCrownWidthEquations(equations)
        )
    return UNSET
