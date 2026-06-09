"""
fastfuels_sdk/v2/modifications.py

Modification primitives for grid creation.

A grid modification is a rule applied to a grid *after* it is built from its
source: it pairs *conditions* (spatial or value tests) with *actions* that
rewrite band values for the cells those conditions select. The generated
models (``GridModification``, ``GridFeatureSpatialCondition``,
``GridModificationAction``) express the full vocabulary; ``mask`` is the one
primitive the core grids workflow needs and the v2 replacement for v1's
``feature_masks``.
"""

from typing import List, Optional, Union

from fastfuels_sdk.v2.client_library.models import (
    GridFeatureSpatialCondition,
    GridModification,
    GridModificationAction,
    GridSpatialTarget,
    Modifier,
    SpatialOperator,
)
from fastfuels_sdk.v2.client_library.types import UNSET

__all__ = ["mask"]


def _feature_id(feature) -> str:
    """Accept a ``Feature`` record or a bare id string."""
    return getattr(feature, "id", feature)


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
