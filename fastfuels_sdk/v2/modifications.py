"""
fastfuels_sdk/v2/modifications.py

Modification primitives for grids and tree inventories.

A modification is a rule applied to a resource: it pairs *conditions* (spatial
or value tests, all ANDed) with *actions* applied to whatever the conditions
select. ``mask`` builds a grid modification (the v2 replacement for v1's
``feature_masks``); ``tree_attribute`` / ``tree_within`` / ``remove_trees`` /
``modify_trees`` build inventory modifications so callers don't hand-assemble
the generated models.
"""

from typing import List, Optional, Union

from fastfuels_sdk.v2.client_library.models import (
    GridFeatureSpatialCondition,
    GridModification,
    GridModificationAction,
    GridSpatialTarget,
    InventoryAttribute,
    InventoryFeatureSpatialCondition,
    InventoryModification,
    InventoryModificationAction,
    InventoryModificationCondition,
    Modifier,
    Operator,
    RemoveAction,
    SpatialOperator,
)
from fastfuels_sdk.v2.client_library.types import UNSET

__all__ = [
    "mask",
    "tree_attribute",
    "tree_within",
    "remove_trees",
    "modify_trees",
]

# Comparison operators accept both their enum names and the symbolic forms.
_OPERATORS = {
    "<": Operator.LT,
    "lt": Operator.LT,
    "<=": Operator.LE,
    "le": Operator.LE,
    ">": Operator.GT,
    "gt": Operator.GT,
    ">=": Operator.GE,
    "ge": Operator.GE,
    "==": Operator.EQ,
    "eq": Operator.EQ,
    "!=": Operator.NE,
    "ne": Operator.NE,
}


def _feature_id(feature) -> str:
    """Accept a ``Feature`` record or a bare id string."""
    return getattr(feature, "id", feature)


def _operator(operator) -> Operator:
    """Coerce a symbolic ("<") or named ("lt") operator, or enum member."""
    if isinstance(operator, Operator):
        return operator
    try:
        return _OPERATORS[operator]
    except (KeyError, TypeError):
        raise ValueError(
            f"Unknown operator {operator!r}. Use one of "
            f"{sorted(_OPERATORS)} or an Operator member."
        )


def mask(
    feature,
    band: Union[str, List[str]],
    value: Union[float, int, str] = 0.0,
    *,
    operator: str = "within",
    buffer_m: Optional[float] = None,
    target: Optional[str] = None,
) -> GridModification:
    """Build a modification that overwrites a band where cells fall within a feature.

    Pass a completed feature (road, water, or layerset) in the same domain as
    the grid, and every grid cell selected by the spatial ``operator`` has
    ``band`` replaced with ``value``. The returned modification is suitable for
    the ``modifications=`` argument of any grid creator.

    Parameters
    ----------
    feature : Feature or str
        The feature to mask against, or its id. Must be ``completed`` and
        belong to the same domain as the grid being modified.
    band : str or list of str
        The band(s) to overwrite, using dot-notation keys (e.g. ``"fbfm"``,
        ``"fuel_load.1hr"``). A list applies the same value to every band.
    value : float, int, or str, default 0.0
        The replacement value written to ``band`` for matching cells.
    operator : {"within", "intersects", "outside"}, default "within"
        Which cells to select relative to the feature geometry.
    buffer_m : float, optional
        Buffer applied to the feature geometry, in meters in the domain's
        projected CRS, before testing. Linestring features such as roads
        usually need a buffer — or ``target="cell"`` — to catch the cells they
        cross. Defaults to no buffer.
    target : {"centroid", "cell"}, optional
        Which part of each grid cell is tested against the geometry. Defaults
        to the API default (``"centroid"``). Use ``"cell"`` to select every
        cell a geometry touches.

    Returns
    -------
    GridModification
        A modification to pass in a creator's ``modifications=`` list.

    Examples
    --------
    Mask roads to a non-burnable fuel model code, buffering the linestrings so
    they cover whole cells:

    >>> import fastfuels_sdk.v2 as ff
    >>> roads = ff.features.create_road_feature_from_osm(domain)
    >>> roads.wait()
    >>> grid = ff.grids.create_fuel_model_grid_from_landfire_fbfm40(
    ...     domain,
    ...     output_resolution_m=30,
    ...     modifications=[ff.mask(roads, "fbfm", 91, buffer_m=5)],
    ... )
    """
    bands = [band] if isinstance(band, str) else list(band)
    condition = GridFeatureSpatialCondition(
        source="feature",
        operator=SpatialOperator(operator),
        feature_id=_feature_id(feature),
        buffer_m=buffer_m if buffer_m is not None else UNSET,
        target=GridSpatialTarget(target) if target is not None else UNSET,
    )
    actions = [
        GridModificationAction(band=b, modifier=Modifier.REPLACE, value=value)
        for b in bands
    ]
    return GridModification(conditions=[condition], actions=actions)


# ---------------------------------------------------------------------------
# Tree-inventory modifications
# ---------------------------------------------------------------------------
#
# An inventory modification pairs conditions (ANDed) with actions applied to
# the matching trees. ``tree_attribute`` / ``tree_within`` build conditions;
# ``remove_trees`` / ``modify_trees`` assemble the modification. Pass the result
# to a tree-inventory creator's ``modifications=`` argument or to
# ``Inventory.apply_modifications``.


def tree_attribute(attribute, operator, value, *, unit: Optional[str] = None):
    """Build a condition testing a per-tree attribute.

    Parameters
    ----------
    attribute : str
        The tree attribute to test: "dbh", "height", "crown_ratio", or
        "fia_species_code" (an ``InventoryAttribute`` member is also accepted).
    operator : str
        A comparison: ``"<"``, ``"<="``, ``">"``, ``">="``, ``"=="``, ``"!="``
        (or the names ``"lt"``, ``"le"``, ``"gt"``, ``"ge"``, ``"eq"``,
        ``"ne"``; an ``Operator`` member is also accepted).
    value : float, int, str, or list
        The value to compare against.
    unit : str, optional
        Unit of ``value`` if not the attribute's default.

    Returns
    -------
    InventoryModificationCondition
        A condition for ``remove_trees`` / ``modify_trees``.
    """
    return InventoryModificationCondition(
        attribute=_tree_attribute(attribute),
        operator=_operator(operator),
        value=value,
        unit=unit if unit is not None else UNSET,
    )


def tree_within(feature, *, buffer_m: Optional[float] = None, operator: str = "within"):
    """Build a condition selecting trees by their location relative to a feature.

    Parameters
    ----------
    feature : Feature or str
        The feature to test against, or its id. Must be ``completed`` and in
        the same domain as the inventory.
    buffer_m : float, optional
        Buffer applied to the feature geometry, in meters in the domain's
        projected CRS, before testing.
    operator : {"within", "intersects", "outside"}, default "within"
        Which trees to select relative to the feature geometry.

    Returns
    -------
    InventoryFeatureSpatialCondition
        A condition for ``remove_trees`` / ``modify_trees``.
    """
    return InventoryFeatureSpatialCondition(
        source="feature",
        operator=SpatialOperator(operator),
        feature_id=_feature_id(feature),
        buffer_m=buffer_m if buffer_m is not None else UNSET,
    )


def remove_trees(*conditions) -> InventoryModification:
    """Build a modification that removes the trees matching every condition.

    Parameters
    ----------
    *conditions
        One or more conditions from :func:`tree_attribute` / :func:`tree_within`
        (ANDed). At least one is required.

    Returns
    -------
    InventoryModification
        For a creator's ``modifications=`` list or
        :meth:`Inventory.apply_modifications`.

    Examples
    --------
    >>> import fastfuels_sdk.v2 as ff
    >>> inventory.apply_modifications([ff.remove_trees(ff.tree_attribute("dbh", "<", 10))])
    """
    if not conditions:
        raise ValueError("remove_trees requires at least one condition.")
    return InventoryModification(conditions=list(conditions), actions=[RemoveAction()])


def modify_trees(
    attribute, modifier, value, *conditions, unit: Optional[str] = None
) -> InventoryModification:
    """Build a modification that changes an attribute on the matching trees.

    Parameters
    ----------
    attribute : str
        The attribute to change ("dbh", "height", "crown_ratio",
        "fia_species_code"; an ``InventoryAttribute`` member is also accepted).
    modifier : str
        How to change it: "replace", "add", "subtract", "multiply", or
        "divide" (a ``Modifier`` member is also accepted). To drop trees, use
        :func:`remove_trees` instead.
    value : float, int, or str
        The operand for ``modifier``.
    *conditions
        One or more conditions from :func:`tree_attribute` / :func:`tree_within`
        (ANDed). At least one is required.
    unit : str, optional
        Unit of ``value`` if not the attribute's default.

    Returns
    -------
    InventoryModification
        For a creator's ``modifications=`` list or
        :meth:`Inventory.apply_modifications`.

    Examples
    --------
    >>> import fastfuels_sdk.v2 as ff
    >>> inventory.apply_modifications([
    ...     ff.modify_trees("height", "multiply", 0.9, ff.tree_attribute("dbh", ">", 0))
    ... ])
    """
    if not conditions:
        raise ValueError("modify_trees requires at least one condition.")
    action = InventoryModificationAction(
        attribute=_tree_attribute(attribute),
        modifier=Modifier(modifier),
        value=value,
        unit=unit if unit is not None else UNSET,
    )
    return InventoryModification(conditions=list(conditions), actions=[action])


def _tree_attribute(attribute) -> InventoryAttribute:
    """Coerce a string or enum member to an ``InventoryAttribute``."""
    if isinstance(attribute, InventoryAttribute):
        return attribute
    return InventoryAttribute(attribute)
