"""
fastfuels_sdk/v2/draft_grids_opc.py

DRAFT — Grid wrapper built on the **openapi-python-client** client
(`client_library`: attrs models + httpx).

Part of the v2 client-library generator comparison; see COMPARISON.md.
Covers a representative slice of the grid endpoints: LANDFIRE FBFM40,
TreeMap (PIM), and 3DEP topography (elevation) creation, plus the
get/wait/delete/list lifecycle shared by all grid sources.
"""

import json
import time
from typing import Any, List, Optional

import attrs

# NOTE (comparison): one AuthenticatedClient serves every resource — no
# per-resource API objects, so the domains draft's client is reused as-is.
from fastfuels_sdk.v2.draft_domains_opc import _checked, get_client

from fastfuels_sdk.v2.client_library.api.grids import (
    create_3dep_topography,
    create_landfire_fbfm40,
    create_treemap,
    delete_grid,
    get_grid,
    list_grids as list_grids_endpoint,
)
from fastfuels_sdk.v2.client_library.models import (
    Grid as GridModel,
    CreateLandfireFbfm40Request,
    CreateThreeDepTopographyRequest,
    CreateTreeMapRequest,
    JobStatus,
    ListGridsResponse,
)

V2_BASE_URL = "https://api-v2-prod-782971006568.us-west1.run.app"


def _base_request_dict(
    name: str,
    description: str,
    tags: Optional[List[str]],
    extent_buffer_cells: int,
) -> dict:
    """Build the request fields shared by every grid creation endpoint."""
    body: dict[str, Any] = {
        "name": name,
        "description": description,
        "extent_buffer_cells": extent_buffer_cells,
    }
    if tags is not None:
        body["tags"] = tags
    return body


class Grid(GridModel):
    """Grid resource for the FastFuels v2 API (openapi-python-client draft).

    Inherits all attributes from the generated attrs model: id, domain_id,
    name, description, status, progress, source, bands, georeference,
    modifications, error, chunks, tags, created_on, modified_on.

    v2 unifies all grid types (surface/tree/topography/feature in v1) into
    one job-based Grid resource distinguished by its `source`.
    """

    @classmethod
    def _from_model(cls, model: GridModel) -> "Grid":
        # The idiomatic opc conversion: round-trip through the generated
        # to_dict/from_dict (from_dict constructs `cls`, i.e. this subclass).
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: GridModel) -> "Grid":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(GridModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    @classmethod
    def from_id(cls, domain_id: str, grid_id: str) -> "Grid":
        """Retrieve an existing Grid by domain and grid ID."""
        response = get_grid.sync(domain_id, grid_id, client=get_client())
        return cls._from_model(_checked(response, GridModel))

    @classmethod
    def create_landfire_fbfm40(
        cls,
        domain_id: str,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        extent_buffer_cells: int = 0,
        version: str = "2024",
        remove_non_burnable: Optional[List[str]] = None,
    ) -> "Grid":
        """Create a surface fuel model grid from LANDFIRE FBFM40."""
        body = _base_request_dict(name, description, tags, extent_buffer_cells)
        body["version"] = str(version)  # version enums are strings
        if remove_non_burnable is not None:
            body["remove_non_burnable"] = remove_non_burnable
        request = CreateLandfireFbfm40Request.from_dict(body)
        response = create_landfire_fbfm40.sync(
            domain_id, client=get_client(), body=request
        )
        return cls._from_model(_checked(response, GridModel))

    @classmethod
    def create_treemap(
        cls,
        domain_id: str,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        extent_buffer_cells: int = 0,
        version: str = "2022",
        bands: Optional[List[str]] = None,
    ) -> "Grid":
        """Create a plot identification (PIM) grid from TreeMap."""
        body = _base_request_dict(name, description, tags, extent_buffer_cells)
        body["version"] = str(version)  # version enums are strings
        if bands is not None:
            body["bands"] = bands  # API default: ["tm_id"]
        request = CreateTreeMapRequest.from_dict(body)
        response = create_treemap.sync(domain_id, client=get_client(), body=request)
        return cls._from_model(_checked(response, GridModel))

    @classmethod
    def create_3dep_topography(
        cls,
        domain_id: str,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        extent_buffer_cells: int = 0,
        source_resolution: int = 10,
        bands: Optional[List[str]] = None,
    ) -> "Grid":
        """Create an elevation/topography grid from USGS 3DEP."""
        body = _base_request_dict(name, description, tags, extent_buffer_cells)
        body["source_resolution"] = source_resolution
        if bands is not None:
            body["bands"] = bands  # API default: ["elevation"]
        request = CreateThreeDepTopographyRequest.from_dict(body)
        response = create_3dep_topography.sync(
            domain_id, client=get_client(), body=request
        )
        return cls._from_model(_checked(response, GridModel))

    def get(self, in_place: bool = False) -> "Grid":
        """Retrieve the latest grid data from the API."""
        response = _checked(
            get_grid.sync(self.domain_id, self.id, client=get_client()),
            GridModel,
        )
        if in_place:
            return self._copy_fields_from(response)
        return Grid._from_model(response)

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> "Grid":
        """Poll the grid job until it reaches a terminal status.

        Raises TimeoutError if the job does not finish within `timeout`
        seconds, or RuntimeError if the job ends in `failed` status.
        """
        elapsed = 0.0
        grid = self.get()
        while grid.status not in (JobStatus.COMPLETED, JobStatus.FAILED):
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Grid {self.id} did not complete within {timeout} seconds"
                )
            time.sleep(step)
            elapsed += step
            grid = self.get()
            if verbose:
                print(f"Grid {self.id}: {grid.status} ({elapsed:.0f}s)")
        if grid.status == JobStatus.FAILED:
            raise RuntimeError(f"Grid {self.id} failed: {grid.error}")
        if in_place:
            return self._copy_fields_from(grid)
        return grid

    def delete(self) -> None:
        """Delete this grid."""
        delete_grid.sync_detailed(self.domain_id, self.id, client=get_client())

    def to_json(self) -> str:
        """Serialize the complete Grid object to a JSON string."""
        return json.dumps(self.to_dict(), default=str, indent=2)


def list_grids(
    domain_id: str,
    page: int = 0,
    size: int = 100,
) -> List[Grid]:
    """List grids in a domain (single page)."""
    response = _checked(
        list_grids_endpoint.sync(domain_id, client=get_client(), page=page, size=size),
        ListGridsResponse,
    )
    return [Grid._from_model(g) for g in response.grids]
