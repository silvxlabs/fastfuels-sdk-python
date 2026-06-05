"""
fastfuels_sdk/v2/draft_inventories_opc.py

DRAFT — Inventory wrapper built on the **openapi-python-client** client
(`client_library`: attrs models + httpx).

Part of the v2 client-library generator comparison; see COMPARISON.md.
Covers the PIM grid → tree inventory flow plus the get/wait/delete/list
lifecycle.

The full PIM workflow across the drafts:

    grid = Grid.create_treemap(domain_id)            # draft_grids_opc
    grid.wait_until_completed()
    inv = Inventory.create_from_pim_grid(domain_id, grid.id)
    inv.wait_until_completed()
"""

import json
import time
from typing import Any, List, Optional

import attrs

from fastfuels_sdk.v2.draft_domains_opc import _checked, get_client

from fastfuels_sdk.v2.client_library.api.inventories import (
    create_pim_inventory,
    delete_inventory,
    get_inventory,
    list_inventories as list_inventories_endpoint,
)
from fastfuels_sdk.v2.client_library.models import (
    Inventory as InventoryModel,
    CreatePimInventoryRequest,
    JobStatus,
    ListInventoriesResponse,
)

V2_BASE_URL = "https://api-v2-prod-782971006568.us-west1.run.app"


class Inventory(InventoryModel):
    """Inventory resource for the FastFuels v2 API (openapi-python-client draft).

    Inherits all attributes from the generated attrs model: id, domain_id,
    type_, name, description, status, progress, source, modifications,
    treatments, columns, georeference, error, tags, created_on,
    modified_on.
    """

    @classmethod
    def _from_model(cls, model: InventoryModel) -> "Inventory":
        return cls.from_dict(model.to_dict())

    def _copy_fields_from(self, model: InventoryModel) -> "Inventory":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(InventoryModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        self.additional_properties = dict(model.additional_properties)
        return self

    @classmethod
    def from_id(cls, domain_id: str, inventory_id: str) -> "Inventory":
        """Retrieve an existing Inventory by domain and inventory ID."""
        response = get_inventory.sync(domain_id, inventory_id, client=get_client())
        return cls._from_model(_checked(response, InventoryModel))

    @classmethod
    def create_from_pim_grid(
        cls,
        domain_id: str,
        source_pim_grid_id: str,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        seed: Optional[int] = None,
        point_process: str = "inhomogeneous_poisson",
    ) -> "Inventory":
        """Create a tree inventory from a completed PIM (TreeMap) grid.

        The PIM grid must be in `completed` status before the inventory
        job can sample tree records from it.
        """
        body: dict[str, Any] = {
            "name": name,
            "description": description,
            "source_pim_grid_id": source_pim_grid_id,
            "point_process": point_process,
        }
        if tags is not None:
            body["tags"] = tags
        if seed is not None:
            body["seed"] = seed
        request = CreatePimInventoryRequest.from_dict(body)
        response = create_pim_inventory.sync(
            domain_id, client=get_client(), body=request
        )
        return cls._from_model(_checked(response, InventoryModel))

    def get(self, in_place: bool = False) -> "Inventory":
        """Retrieve the latest inventory data from the API."""
        response = _checked(
            get_inventory.sync(self.domain_id, self.id, client=get_client()),
            InventoryModel,
        )
        if in_place:
            return self._copy_fields_from(response)
        return Inventory._from_model(response)

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> "Inventory":
        """Poll the inventory job until it reaches a terminal status."""
        elapsed = 0.0
        inventory = self.get()
        while inventory.status not in (JobStatus.COMPLETED, JobStatus.FAILED):
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Inventory {self.id} did not complete within {timeout} seconds"
                )
            time.sleep(step)
            elapsed += step
            inventory = self.get()
            if verbose:
                print(f"Inventory {self.id}: {inventory.status} ({elapsed:.0f}s)")
        if inventory.status == JobStatus.FAILED:
            raise RuntimeError(f"Inventory {self.id} failed: {inventory.error}")
        if in_place:
            return self._copy_fields_from(inventory)
        return inventory

    def delete(self) -> None:
        """Delete this inventory."""
        delete_inventory.sync_detailed(self.domain_id, self.id, client=get_client())

    def to_json(self) -> str:
        """Serialize the complete Inventory object to a JSON string."""
        return json.dumps(self.to_dict(), default=str, indent=2)


def list_inventories(
    domain_id: str,
    page: int = 0,
    size: int = 100,
) -> List[Inventory]:
    """List inventories in a domain (single page)."""
    response = _checked(
        list_inventories_endpoint.sync(
            domain_id, client=get_client(), page=page, size=size
        ),
        ListInventoriesResponse,
    )
    return [Inventory._from_model(i) for i in response.inventories]
