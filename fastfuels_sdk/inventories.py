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

    def get(self, in_place: bool = False):
        """
        Fetches the inventory data associated with the domain ID.

        This method interacts with the API to fetch the inventory data associated with the domain ID.
        The fetched data is then used to update the `Inventories` object.

        Parameters
        ----------
        in_place : bool, optional
            If `True`, the method updates the current object with the fetched data.
            If `False`, the method returns a new object with the fetched data.
            Default is `False`.

        Returns
        -------
        Inventories
            An instance of `Inventories` updated with the fetched inventory data.

        Examples
        --------
        >>> from fastfuels_sdk import Domain, Inventories
        >>> my_domain = Domain.from_id("domain_id")
        >>> inventories = Inventories.from_domain(my_domain)
        >>> # Fetch and update the inventory data
        >>> updated_inventories = inventories.get()
        >>> # Fetch and update the inventory data in place
        >>> inventories.get(in_place=True)
        """
        response = _INVENTORIES_API.get_inventories(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return Inventories(domain_id=self.domain_id, **response.model_dump())


class TreeInventory(TreeInventoryModel):
    pass
