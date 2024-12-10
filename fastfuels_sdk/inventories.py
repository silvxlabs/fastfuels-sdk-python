"""
inventories.py
"""

# Core imports
from __future__ import annotations
from typing import Optional

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.domains import Domain
from fastfuels_sdk.client_library.api import InventoriesApi, TreeInventoryApi
from fastfuels_sdk.client_library.models import (
    Inventories as InventoriesModel,
    TreeInventory as TreeInventoryModel,
    CreateTreeInventoryRequest,
    TreeMapSource,
    TreeMapVersion,
    TreeInventorySource,
    TreeInventoryModification,
    CreateTreeInventoryRequestTreatmentsInner as CreateTreeInventoryRequestTreatments,
)

_INVENTORIES_API = InventoriesApi(get_client())
_TREE_INVENTORY_API = TreeInventoryApi(get_client())


class Inventories(InventoriesModel):
    """
    This class serves as an interface for interacting with the inventory data associated
    with a particular domain. It provides methods to fetch, update, and initialize inventory
    data from the API.

    Attributes
    ----------
    domain_id : str
        The ID of the domain associated with the inventory.
    tree : TreeInventory, optional
        The tree inventory data associated with the domain. By default, this attribute is `None`.
    """

    domain_id: str
    tree: Optional[TreeInventory]  # Override the default TreeInventoryModel type

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

    def create_tree_inventory(
        self,
        sources: list[str],
        tree_map: TreeMapSource,
        modifications: list[TreeInventoryModification],
        treatments: list[CreateTreeInventoryRequestTreatments],
        feature_masks: list[str],
    ) -> TreeInventory:
        """ """

    def create_tree_inventory_from_treemap(
        self,
        version: str = "2016",
        seed: int = None,
        in_place: bool = False,
        modifications: list[dict] = None,
        treatments: list[dict] = None,
    ) -> TreeInventory:
        """Create a tree inventory using TreeMap data for the current domain.

        This method generates a new tree inventory using TreeMap, which provides nationwide
        coverage of tree data. The generated inventory includes information about tree
        species, sizes, and locations within your domain.



        Parameters
        ----------
        version : str, optional
            The TreeMap version to use for generating the inventory. Available versions:
            - "2016" (default) - Uses the 2016 TreeMap dataset
            - "2014" - Uses the 2014 TreeMap dataset

        seed : int, optional
            A random seed for reproducible tree inventory generation. If not provided,
            a random seed will be used, resulting in different trees each time.

        in_place : bool, optional
            Controls whether to update the current Inventories object:
            - If True, updates this object's tree inventory (self.tree)
            - If False (default), leaves this object unchanged

        Returns
        -------
        TreeInventory
            The newly created tree inventory object, regardless of the in_place setting.

        Notes
        -----
        - The inventory generation happens asynchronously. When this method returns,
          the inventory will be in a "pending" state. You'll need to check its status
          to know when it's ready for use.
        - TreeMap provides nationwide coverage but may have varying accuracy in
          different regions.
        - Using the same seed value will generate the same trees when all other
          parameters are identical.

        Example
        -------
        >>> from fastfuels_sdk import Domain, Inventories
        >>> my_domain = Domain.from_id("domain_id")
        >>> inventories = Inventories.from_domain(my_domain)
        >>> # Create a new tree inventory without modifying the current object
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap()
        >>>
        >>> # Create a tree inventory and update the current object
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(in_place=True)
        >>>
        >>> # Create with a specific TreeMap version and seed
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     version="2014",
        ...     seed=42,
        ... )
        """
        treemap_request = TreeMapSource(version=TreeMapVersion(version), seed=seed)
        request_body = CreateTreeInventoryRequest(
            sources=[TreeInventorySource.TREEMAP],
            tree_map=treemap_request,
            modifications=modifications,
            treatments=treatments,
        )
        response = _TREE_INVENTORY_API.create_tree_inventory(
            self.domain_id, request_body
        )
        tree_inventory = TreeInventory(**response.model_dump())

        if in_place:
            self.tree = tree_inventory

        return tree_inventory


class TreeInventory(TreeInventoryModel):
    """ """

    # @classmethod
    # def from_treemap(
    #     cls, domain: Domain, version: str = "2016", seed: int = None
    # ) -> TreeInventory:
    #     treemap_request = TreeMapSource(version=TreeMapVersion(version), seed=seed)
    #     request_body = CreateTreeInventoryRequest(
    #         sources=[TreeInventorySource.TREEMAP], tree_map=treemap_request
    #     )
    #     response = _TREE_INVENTORY_API.create_tree_inventory(domain.id, request_body)
    #     return cls(**response.model_dump())
