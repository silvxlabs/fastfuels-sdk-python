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
    TreeInventoryTreatment,
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

    @staticmethod
    def _parse_inventory_items(
        items,
        item_class,
    ):
        """Parse inventory modifications or treatments into the correct format before sending to the API.

        Parameters
        ----------
        items : dict or list[dict] or None
            Raw items to parse. Each item should be a dictionary containing
            the required fields for the specified item_class.

        item_class : type
            Class to parse items into (TreeInventoryModification or TreeInventoryTreatment)

        Returns
        -------
        list or None
            Parsed items in the correct format, or None if input was None
        """
        if items is None:
            return None

        if isinstance(items, dict):
            items = [items]

        return [item_class.from_dict(item) for item in items]  # type: ignore

    def create_tree_inventory(
        self,
        sources: str | list[str] | TreeInventorySource | list[TreeInventorySource],
        tree_map: Optional[TreeMapSource | dict] = None,
        modifications: Optional[dict | list[dict]] = None,
        treatments: Optional[dict | list[dict]] = None,
        feature_masks: Optional[str | list[str]] = None,
        in_place: bool = False,
    ) -> TreeInventory:
        """Create a tree inventory for the current domain.

        This method generates a tree inventory using specified data sources and configurations.
        A tree inventory represents a complete forest inventory within the spatial context
        of your domain. Currently, TreeMap is the primary supported data source, providing
        nationwide coverage of tree data.

        Parameters
        ----------
        sources : str or list[str] or TreeInventorySource
            Data source(s) to use for the tree inventory. Currently supports:
            - "TreeMap": Uses the TreeMap raster product for nationwide coverage

        tree_map : TreeMapSource or dict, optional
            Configuration for TreeMap source if being used. Can be provided as a dict with:
            - version: "2014" or "2016" (default: "2016")
            - seed: Integer for reproducible generation (optional)

        modifications : dict or list[dict], optional
            List of modifications to apply. Each modification has:
            - conditions: List of conditions that must be met
            - actions: List of actions to apply when conditions are met

            Example:
            ```python
            {
                "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
                "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
            }
            ```

        treatments : dict or list[dict], optional
            List of silvicultural treatments to apply. Supports:

            Proportional Thinning:
            ```python
            {
                "method": "proportionalThinning",
                "targetMetric": "basalArea",
                "targetValue": 25.0  # in m²/ha
            }
            ```

            Directional Thinning:
            ```python
            {
                "method": "directionalThinning",
                "direction": "below",  # or "above"
                "targetMetric": "diameter",  # or "basalArea"
                "targetValue": 30.0  # cm for diameter, m²/ha for basalArea
            }
            ```

        feature_masks : str or list[str], optional
            Features to mask out from the inventory.
            Supported values: ["road", "water"]

        in_place : bool, optional
            If True, updates this object's tree inventory (self.tree).
            If False (default), leaves this object unchanged.

        Returns
        -------
        TreeInventory
            The newly created tree inventory object.

        Notes
        -----
        - The inventory generation happens asynchronously. The returned inventory
          will initially have a "pending" status.
        - Using the same seed value will generate the same trees when all other
          parameters are identical.

        Examples
        --------
        >>> from fastfuels_sdk import Domain, Inventories
        >>> my_domain = Domain.from_id("domain_id")
        >>> inventories = Inventories.from_domain(my_domain)

        Basic usage with TreeMap:
        >>> inventory = inventories.create_tree_inventory(sources="TreeMap")

        Specify TreeMap version and seed:
        >>> inventory = inventories.create_tree_inventory(
        ...     sources="TreeMap",
        ...     tree_map={"version": "2014", "seed": 42}
        ... )

        Add height modification:
        >>> inventory = inventories.create_tree_inventory(
        ...     sources="TreeMap",
        ...     modifications={
        ...         "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
        ...         "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
        ...     }
        ... )

        Add proportional thinning treatment:
        >>> inventory = inventories.create_tree_inventory(
        ...     sources="TreeMap",
        ...     treatments={
        ...         "method": "proportionalThinning",
        ...         "targetMetric": "basalArea",
        ...         "targetValue": 25.0
        ...     }
        ... )

        Mask out roads and water:
        >>> inventory = inventories.create_tree_inventory(
        ...     sources="TreeMap",
        ...     feature_masks=["road", "water"]
        ... )
        """

        # Create the request body
        request_body = CreateTreeInventoryRequest(
            sources=[sources] if isinstance(sources, str) else sources,
            tree_map=tree_map,
            modifications=self._parse_inventory_items(
                modifications, TreeInventoryModification
            ),
            treatments=self._parse_inventory_items(treatments, TreeInventoryTreatment),
            feature_masks=(
                [feature_masks] if isinstance(feature_masks, str) else feature_masks
            ),
        )

        # Make API call
        response = _TREE_INVENTORY_API.create_tree_inventory(
            self.domain_id, request_body
        )
        tree_inventory = TreeInventory(**response.model_dump())

        if in_place:
            self.tree = tree_inventory

        return tree_inventory

    def create_tree_inventory_from_treemap(
        self,
        version: str = "2016",
        seed: int = None,
        modifications: Optional[dict | list[dict]] = None,
        treatments: Optional[dict | list[dict]] = None,
        feature_masks: Optional[str | list[str]] = None,
        in_place: bool = False,
    ) -> TreeInventory:
        """Create a tree inventory using TreeMap data for the current domain.

        This is a convenience method that provides a simplified interface for creating
        tree inventories specifically from TreeMap data. While create_tree_inventory()
        offers a more general interface supporting multiple data sources, this method
        is optimized for the common case of using TreeMap data with a focus on the
        most relevant parameters.

        Use this method when:
        - You want to create an inventory using TreeMap data (most common case)
        - You prefer a simpler interface focused on TreeMap-specific parameters
        - You want clearer defaults and documentation for TreeMap usage

        Use create_tree_inventory() instead when:
        - You need to use data sources other than TreeMap
        - You prefer more explicit control over source configuration
        - You need to specify multiple data sources

        Parameters
        ----------
        version : str, optional
            The TreeMap version to use. Available versions:
            - "2016" (default) - More recent dataset, recommended for most use cases
            - "2014" - Earlier dataset, use if you need historical comparison

        seed : int, optional
            Random seed for reproducible tree generation. When provided, generates
            identical trees for the same domain and parameters. If omitted, generates
            different trees each time.

        modifications : dict or list[dict], optional
            Rules for modifying tree attributes. Each modification includes:
            - conditions: List of criteria that trees must meet
            - actions: Changes to apply to matching trees

            Example - Reduce height of tall trees:
            ```python
            {
                "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
                "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
            }
            ```

            Available fields:
            - HT: Height (meters)
            - DIA: Diameter at breast height (centimeters)
            - CR: Crown ratio (0-1)
            - SPCD: Species code (integer)

        treatments : dict or list[dict], optional
            Silvicultural treatments to apply. Supports:

            Proportional Thinning - Reduces stand density to target basal area:
            ```python
            {
                "method": "proportionalThinning",
                "targetMetric": "basalArea",
                "targetValue": 25.0  # Target basal area in m²/ha
            }
            ```

            Directional Thinning - Removes trees based on size:
            ```python
            {
                "method": "directionalThinning",
                "direction": "below",  # "below" or "above"
                "targetMetric": "diameter",  # "diameter" or "basalArea"
                "targetValue": 30.0  # cm for diameter, m²/ha for basalArea
            }
            ```

        feature_masks : str or list[str], optional
            Features to exclude from the inventory by removing trees that intersect with them.
            Available masks:
            - "road": Removes trees on roads
            - "water": Removes trees in water bodies

        in_place : bool, optional
            Controls whether to update the current Inventories object:
            - If True, updates this object's tree inventory (self.tree)
            - If False (default), returns new inventory without modifying current object

        Returns
        -------
        TreeInventory
            The newly created tree inventory object.

        Notes
        -----
        - Generation is asynchronous - the inventory starts in "pending" status
        - Final generation can take several minutes depending on domain size
        - Check inventory.status for current state: "pending", "running", "completed"
        - TreeMap accuracy varies by region and forest type
        - Use same seed value to reproduce exact tree patterns

        Examples
        --------
        >>> from fastfuels_sdk import Domain, Inventories
        >>> my_domain = Domain.from_id("domain_id")
        >>> inventories = Inventories.from_domain(my_domain)

        Basic inventory creation:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap()

        Reproducible inventory with specific version:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     version="2014",
        ...     seed=42
        ... )

        Reduce height of tall trees:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     modifications={
        ...         "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
        ...         "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
        ...     }
        ... )

        Thin to target basal area:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     treatments={
        ...         "method": "proportionalThinning",
        ...         "targetMetric": "basalArea",
        ...         "targetValue": 25.0
        ...     }
        ... )

        Remove trees from roads and water:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     feature_masks=["road", "water"]
        ... )

        Combined modifications, thinning, and masks:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     seed=42,
        ...     modifications={
        ...         "conditions": [{"field": "HT", "operator": "gt", "value": 20}],
        ...         "actions": [{"field": "HT", "modifier": "multiply", "value": 0.9}]
        ...     },
        ...     treatments={
        ...         "method": "proportionalThinning",
        ...         "targetMetric": "basalArea",
        ...         "targetValue": 25.0
        ...     },
        ...     feature_masks=["road", "water"]
        ... )
        """
        tree_map = TreeMapSource(version=TreeMapVersion(version), seed=seed)
        return self.create_tree_inventory(
            sources=[TreeInventorySource.TREEMAP],
            tree_map=tree_map,
            modifications=modifications,
            treatments=treatments,
            feature_masks=feature_masks,
            in_place=in_place,
        )


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
