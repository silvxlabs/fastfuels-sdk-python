"""
inventories.py
"""

from __future__ import annotations

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.domains import Domain
from fastfuels_sdk.client_library.api import InventoriesApi, TreeInventoryApi
from fastfuels_sdk.client_library.models import (
    Inventories as InventoriesModel,
    TreeInventory as TreeInventoryModel,
)

_INVENTORIES_API = InventoriesApi(get_client())
_TREE_INVENTORY_API = TreeInventoryApi(get_client())


class Inventories(InventoriesModel):
    domain_id: str

    @classmethod
    def from_domain(cls, domain: Domain) -> Inventories:
        """
        Constructs an `Inventories` instance from a given `Domain` object.

        This class method interacts with the API to fetch the inventory data associated with the provided domain ID.
        The fetched data is then used to initialize and return an `Inventories` object.

        Parameters
        ----------
        domain : Domain
            The `Domain` object from which to derive the ID for fetching
            inventory data.

        Returns
        -------
        Inventories
            An instance of `Inventories` initialized with inventory data fetched
            using the domain ID.

        Examples
        --------
        >>> from fastfuels_sdk import Domain, Inventories
        >>> my_domain = Domain.from_id("domain_id")
        >>> inventories = Inventories.from_domain(my_domain)
        """
        inventories_response = _INVENTORIES_API.get_inventories(domain_id=domain.id)
        return cls(domain_id=domain.id, **inventories_response.model_dump())


class TreeInventory(TreeInventoryModel):
    pass
