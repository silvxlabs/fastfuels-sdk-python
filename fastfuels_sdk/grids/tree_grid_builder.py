"""
fastfuels_sdk/grids/tree_grid_builder.py
"""

# Core imports
from __future__ import annotations
from typing import List

# Internal imports
from fastfuels_sdk.grids.grids import Grids
from fastfuels_sdk.grids.tree_grid import TreeGrid
from fastfuels_sdk.client_library.models import (
    TreeGridBulkDensitySource,
    TreeGridSPCDSource,
    TreeGridUniformValue,
    TreeGridInventorySource,
)


class TreeGridBuilder:
    """Builder for creating tree grids with complex attribute configurations."""

    def __init__(self, domain_id: str):
        self.domain_id = domain_id
        self.attributes: List[str] = []
        self.config = {}

    def with_bulk_density_from_tree_inventory(self) -> "TreeGridBuilder":
        """Add bulk density attribute from tree inventory data.

        Examples
        --------
        >>> builder = TreeGridBuilder("abc123")
        >>> builder.with_bulk_density_from_tree_inventory()
        """
        self.config["bulk_density"] = TreeGridBulkDensitySource.from_dict(
            TreeGridInventorySource.from_dict({"source": "TreeInventory"}).to_dict()
        ).to_dict()
        self.attributes.append("bulkDensity")

        return self

    def with_uniform_bulk_density(self, value: float) -> "TreeGridBuilder":
        """Set uniform bulk density value.

        Parameters
        ----------
        value : float
            Bulk density value in kg/m³

        Examples
        --------
        >>> builder = TreeGridBuilder("abc123")
        >>> builder.with_uniform_bulk_density(0.5)
        """
        self.config["bulk_density"] = TreeGridBulkDensitySource.from_dict(
            TreeGridUniformValue.from_dict(
                {"source": "uniform", "value": value}
            ).to_dict()
        ).to_dict()
        self.attributes.append("bulkDensity")

        return self

    def with_spcd_from_tree_inventory(self) -> "TreeGridBuilder":
        """Add species code (SPCD) attribute from tree inventory data.

        Examples
        --------
        >>> builder = TreeGridBuilder("abc123")
        >>> builder.with_spcd_from_tree_inventory()
        """
        self.config["spcd"] = TreeGridSPCDSource.from_dict(
            TreeGridInventorySource.from_dict({"source": "TreeInventory"}).to_dict()
        ).to_dict()
        self.attributes.append("SPCD")

        return self

    def with_uniform_fuel_moisture(self, value: float) -> "TreeGridBuilder":
        """Set uniform fuel moisture value.

        Parameters
        ----------
        value : float
            Fuel moisture value (%)

        Examples
        --------
        >>> builder = TreeGridBuilder("abc123")
        >>> builder.with_uniform_fuel_moisture(15.0)  # 15%
        """
        self.config["fuel_moisture"] = TreeGridUniformValue.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append("fuelMoisture")

        return self

    def build(self) -> "TreeGrid":
        """Create the tree grid with configured attributes.

        Examples
        --------
        >>> tree_grid = (TreeGridBuilder("abc123")
        ...     .with_bulk_density_from_tree_inventory()
        ...     .with_spcd_from_tree_inventory()
        ...     .with_uniform_fuel_moisture(15.0)
        ...     .build())
        """
        grid = Grids.from_domain_id(self.domain_id)
        return grid.create_tree_grid(
            attributes=list(set(self.attributes)),  # Remove duplicates
            **self.config,
        )

    def clear(self) -> "TreeGridBuilder":
        """Clear all configured attributes."""
        self.attributes = []
        self.config = {}
        return self

    def to_dict(self) -> dict:
        """Return the dictionary representation of the builder configuration."""
        return {
            "domain_id": self.domain_id,
            "attributes": self.attributes,
            **self.config,
        }
