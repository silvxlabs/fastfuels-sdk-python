"""
fastfuels_sdk/v2/treatments.py

Treatment primitives for tree inventories.

A treatment thins a tree inventory by removing stems until the stand reaches a
target — either a residual basal area or a diameter limit. Pass treatments to a
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
    InventoryBasalAreaTreatment,
    InventoryDiameterTreatment,
    InventoryDiameterTreatmentMethod,
    InventoryTreatmentMethod,
)
from fastfuels_sdk.v2.client_library.types import UNSET

__all__ = ["basal_area_treatment", "diameter_treatment"]


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
