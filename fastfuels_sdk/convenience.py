"""
fastfuels_sdk/convenience.py
"""

# Core imports
from __future__ import annotations
from pathlib import Path

# Internal imports
from fastfuels_sdk.exports import Export
from fastfuels_sdk.domains import Domain
from fastfuels_sdk.grids import Grids
from fastfuels_sdk.features import Features
from fastfuels_sdk.inventories import Inventories
from fastfuels_sdk.grids import (
    TopographyGridBuilder,
    SurfaceGridBuilder,
    TreeGridBuilder,
)

# External imports
from geopandas import GeoDataFrame


def export_roi_to_quicfire(
    roi: GeoDataFrame, export_path: Path | str, verbose: bool = False, **kwargs
) -> Export:
    """Convenience function to export a region of interest (ROI) to QuicFire."""
    # Create a new domain for the ROI
    if verbose:
        print("Creating domain from region of interest")
    domain = Domain.from_geodataframe(roi)

    # Create road and water features for the domain
    if verbose:
        print("Creating road and water features for the domain")
    features = Features.from_domain_id(domain.id)
    road_feature = features.create_road_feature_from_osm()
    water_feature = features.create_water_feature_from_osm()

    # Create a topography grid for the domain
    if verbose:
        print("Creating topography grid for the domain")
    topography_grid = (
        TopographyGridBuilder(domain_id=domain.id)
        .with_elevation_from_3dep(interpolation_method="linear")
        .build()
    )

    # Create feature grid
    road_feature.wait_until_completed(verbose=verbose)
    water_feature.wait_until_completed(verbose=verbose)
    if verbose:
        print("Creating feature grid for the domain")
    feature_grid = Grids.from_domain_id(domain.id).create_feature_grid(
        attributes=["road", "water"]
    )

    # Create a tree inventory for the domain
    if verbose:
        print("Creating tree inventory for the domain")
    tree_inventory = Inventories.from_domain_id(
        domain.id
    ).create_tree_inventory_from_treemap(feature_masks=["road", "water"])

    # Create surface grid
    feature_grid.wait_until_completed(verbose=verbose)
    if verbose:
        print("Creating surface grid for the domain")
    surface_grid = (
        SurfaceGridBuilder(domain_id=domain.id)
        .with_fuel_load_from_landfire(
            product="FBFM40",
            version="2022",
            interpolation_method="cubic",
            curing_live_herbaceous=0.25,
            curing_live_woody=0.1,
            groups=["oneHour"],
            feature_masks=["road", "water"],
            remove_non_burnable=["NB1", "NB2"],
        )
        .with_fuel_depth_from_landfire(
            product="FBFM40",
            version="2022",
            interpolation_method="cubic",
            feature_masks=["road", "water"],
            remove_non_burnable=["NB1", "NB2"],
        )
        .with_uniform_fuel_moisture(value=0.15, feature_masks=["road", "water"])
        .build()
    )

    # Create tree grid
    tree_inventory.wait_until_completed(verbose=verbose)
    if verbose:
        print("Creating tree grid for the domain")
    tree_grid = (
        TreeGridBuilder(domain_id=domain.id)
        .with_bulk_density_from_tree_inventory()
        .build()
    )

    # Create QUIC-Fire Export
    topography_grid.wait_until_completed(verbose=verbose)
    surface_grid.wait_until_completed(verbose=verbose)
    tree_grid.wait_until_completed(verbose=verbose)
    export = Grids.from_domain_id(domain.id).create_export("QUIC-Fire")
    export.wait_until_completed(verbose=verbose)

    # Export the QUIC-Fire data to the specified path
    if verbose:
        print(f"Exporting QUIC-Fire data to {export_path}")
    export_path = Path(export_path) if isinstance(export_path, str) else export_path
    export.wait_until_completed(verbose=verbose, in_place=True)
    export.to_file(export_path)

    return export
