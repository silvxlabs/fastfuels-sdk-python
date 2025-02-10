"""
fastfuels_sdk/grids/topography_grid_builder.py
"""

# Core imports
from __future__ import annotations
from typing import List

# Internal imports
from fastfuels_sdk.grids.grids import Grids
from fastfuels_sdk.grids.topography_grid import TopographyGrid
from fastfuels_sdk.client_library.models import (
    TopographyGridElevationSource,
    TopographyGridAspectSource,
    TopographyGridSlopeSource,
)


class TopographyGridBuilder:
    """Builder for creating topography grids with complex attribute configurations."""

    def __init__(self, domain_id: str):
        self.domain_id = domain_id
        self.attributes: List[str] = []
        self.config = {}

    def with_elevation_from_3dep(
        self, interpolation_method: str = "cubic"
    ) -> "TopographyGridBuilder":
        """Add elevation attribute from 3DEP data."""
        self.config["elevation"] = TopographyGridElevationSource.from_dict(
            {"source": "3DEP", "interpolationMethod": interpolation_method}
        ).to_dict()
        self.attributes.append("elevation")

        return self

    def with_elevation_from_landfire(
        self, interpolation_method: str = "cubic"
    ) -> "TopographyGridBuilder":
        """Add elevation attribute from LANDFIRE data."""
        self.config["elevation"] = TopographyGridElevationSource.from_dict(
            {"source": "LANDFIRE", "interpolationMethod": interpolation_method}
        ).to_dict()
        self.attributes.append("elevation")

        return self

    def with_elevation_from_uniform_value(
        self, value: float
    ) -> "TopographyGridBuilder":
        """Add elevation attribute with uniform value."""
        self.config["elevation"] = TopographyGridElevationSource.from_dict(
            {"source": "uniform", "value": value}
        ).to_dict()
        self.attributes.append("elevation")

        return self

    def with_aspect_from_3dep(self) -> "TopographyGridBuilder":
        """Add aspect attribute from 3DEP data."""
        self.config["aspect"] = TopographyGridAspectSource.from_dict(
            {
                "source": "3DEP",
            }
        ).to_dict()
        self.attributes.append("aspect")

        return self

    def with_aspect_from_landfire(self) -> "TopographyGridBuilder":
        """Add aspect attribute from LANDFIRE data."""
        self.config["aspect"] = TopographyGridAspectSource.from_dict(
            {
                "source": "LANDFIRE",
            }
        ).to_dict()
        self.attributes.append("aspect")

        return self

    def with_slope_from_3dep(
        self, interpolation_method: str = "cubic"
    ) -> "TopographyGridBuilder":
        """Add slope attribute from 3DEP data."""
        self.config["slope"] = TopographyGridSlopeSource.from_dict(
            {"source": "3DEP", "interpolationMethod": interpolation_method}
        ).to_dict()
        self.attributes.append("slope")

        return self

    def with_slope_from_landfire(
        self, interpolation_method: str = "cubic"
    ) -> "TopographyGridBuilder":
        """Add slope attribute from LANDFIRE data."""
        self.config["slope"] = TopographyGridSlopeSource.from_dict(
            {"source": "LANDFIRE", "interpolationMethod": interpolation_method}
        ).to_dict()
        self.attributes.append("slope")

        return self

    def build(self) -> "TopographyGrid":
        """Create the surface grid with configured attributes.

        Examples
        --------
        >>> topography_grid = (TopographyGridBuilder(domain_id="abc123")
        ...     .with_elevation_from_3dep()
        ...     .with_slope_from_3dep()
        ...     .with_aspect_from_landfire()
        ...     .build())
        """
        grid = Grids.from_domain_id(self.domain_id)
        return grid.create_topography_grid(
            attributes=list(set(self.attributes)),  # Remove duplicates
            **self.config,
        )

    def clear(self) -> "TopographyGridBuilder":
        """Clear all configured attributes."""
        self.attributes = []
        self.config = {}
        return self

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "attributes": self.attributes,
            **self.config,
        }
