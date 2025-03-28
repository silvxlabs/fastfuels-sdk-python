"""
inventories.py
"""

# Core imports
from __future__ import annotations
from time import sleep
from pathlib import Path
from typing import Optional

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.utils import parse_dict_items_to_pydantic_list
from fastfuels_sdk.exports import Export
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
    TreeMapSourceCanopyHeightMapConfiguration,
)

# External imports
import requests

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
    def from_domain_id(cls, domain_id: str) -> Inventories:
        """
        Constructs an `Inventories` instance from a given `Domain` object.

        This class method interacts with the API to fetch the inventory data associated with the provided domain ID.
        The fetched data is then used to initialize and return an `Inventories` object.

        Parameters
        ----------
        domain_id : str
            The ID of the domain to fetch inventory data for.

        Returns
        -------
        Inventories
            An instance of `Inventories` initialized with inventory data fetched
            using the domain ID.

        Examples
        --------
        >>> from fastfuels_sdk import Inventories
        >>> inventories = Inventories.from_domain_id("abc123")
        """
        inventories_response = _INVENTORIES_API.get_inventories(domain_id=domain_id)
        response_data = inventories_response.model_dump()
        response_data = _convert_api_models_to_sdk_classes(domain_id, response_data)

        return cls(domain_id=domain_id, **response_data)

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
        >>> from fastfuels_sdk import Inventories
        >>> inventories = Inventories.from_domain_id("abc123")
        >>> # Fetch and update the inventory data
        >>> updated_inventories = inventories.get()
        >>> # Fetch and update the inventory data in place
        >>> inventories.get(in_place=True)
        """
        response = _INVENTORIES_API.get_inventories(domain_id=self.domain_id)
        response_data = response.model_dump()
        response_data = _convert_api_models_to_sdk_classes(
            self.domain_id, response_data
        )

        if in_place:
            # Update all attributes of current instance
            for key, value in response_data.items():
                setattr(self, key, value)
            return self
        return Inventories(domain_id=self.domain_id, **response_data)

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
        >>> from fastfuels_sdk import Inventories
        >>> inventories = Inventories.from_domain_id("abc123")

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
        request_body = CreateTreeInventoryRequest(
            sources=[sources] if isinstance(sources, str) else sources,
            tree_map=tree_map,
            modifications=parse_dict_items_to_pydantic_list(
                modifications, TreeInventoryModification
            ),
            treatments=parse_dict_items_to_pydantic_list(
                treatments, TreeInventoryTreatment
            ),
            feature_masks=(
                [feature_masks] if isinstance(feature_masks, str) else feature_masks
            ),
        )
        response = _TREE_INVENTORY_API.create_tree_inventory(
            self.domain_id, request_body
        )
        tree_inventory = TreeInventory(
            domain_id=self.domain_id, **response.model_dump()
        )
        if in_place:
            self.tree = tree_inventory

        return tree_inventory

    def create_tree_inventory_from_treemap(
        self,
        version: str = "2016",
        seed: int = None,
        canopy_height_map_source: Optional[str] = None,
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
        >>> from fastfuels_sdk import Inventories
        >>> inventories = Inventories.from_domain_id("abc123")

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

        Apply a high resolution canopy height map data fusion:
        >>> tree_inventory = inventories.create_tree_inventory_from_treemap(
        ...     canopy_height_map_source="Meta2024"
        ... )
        """
        if canopy_height_map_source:
            canopy_height_map_configuration = (
                TreeMapSourceCanopyHeightMapConfiguration.from_dict(
                    {"source": canopy_height_map_source}
                )
            )
        else:
            canopy_height_map_configuration = None

        return self.create_tree_inventory(
            sources=[TreeInventorySource.TREEMAP],
            tree_map=TreeMapSource(
                version=TreeMapVersion(version),
                seed=seed,
                canopyHeightMapConfiguration=canopy_height_map_configuration,
            ),
            modifications=modifications,
            treatments=treatments,
            feature_masks=feature_masks,
            in_place=in_place,
        )

    def create_tree_inventory_from_file_upload(
        self,
        file_path: Path | str,
    ) -> TreeInventory:
        """
        Create a tree inventory using a file upload for the current domain.

        This method uploads a CSV file containing tree inventory data and creates a new
        tree inventory for the domain. The file must follow specific format requirements
        and contain required columns with appropriate data types.

        Parameters
        ----------
        file_path : Path or str
            Path to the CSV file containing the tree inventory data.
            The file must include the following columns:
            - TREE_ID (Integer): Unique identifier for each tree
            - SPCD (Integer): FIA species code
            - STATUSCD (Integer): Tree status code (0: No status, 1: Live, 2: Dead, 3: Missing)
            - DIA (Float): Diameter at breast height in cm (0-1200 cm, nullable)
            - HT (Float): Tree height in meters (0-116 m, nullable)
            - CR (Float): Crown ratio (0-1, nullable)
            - X (Float): X coordinate in projected coordinate system (nullable)
            - Y (Float): Y coordinate in projected coordinate system (nullable)

        Returns
        -------
        TreeInventory
            A TreeInventory object representing the newly created inventory.
            The inventory starts in "pending" status and is processed asynchronously.
            Use wait_until_completed() to wait for processing to finish.

        Raises
        ------
        FileNotFoundError
            If the specified file_path does not exist.
        ValueError
            If the file size exceeds 500MB or if the file is not a CSV.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import Inventories
        >>> from pathlib import Path
        >>> inventories = Inventories.from_domain_id("abc123")
        >>> file_path = Path("my_trees.csv")
        >>> # Create and wait for inventory
        >>> inventory = inventories.create_tree_inventory_from_file_upload(file_path)
        >>> inventory = inventory.wait_until_completed()
        >>> print(inventory.status)
        'completed'

        Notes
        -----
        File Format Requirements:
        - Maximum file size: 500MB
        - File type: CSV
        - Must include all required columns with correct data types
        - TREE_ID must be unique integers
        - Values must be within specified ranges
        - Trees must fall within domain bounds
        """
        # Convert string path to Path object if needed
        file_path = Path(file_path)

        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check file size (500MB limit)
        max_size = 500 * 1024 * 1024  # 500MB in bytes
        if file_path.stat().st_size > max_size:
            raise ValueError(f"File size exceeds 500MB limit: {file_path}")

        # Check file extension
        if file_path.suffix.lower() != ".csv":
            raise ValueError(f"File must be a CSV: {file_path}")

        # Create tree inventory resource with "file" source
        signed_url_response = _TREE_INVENTORY_API.create_tree_inventory(
            self.domain_id,
            CreateTreeInventoryRequest(sources=[TreeInventorySource.FILE]),
        )

        # Read file content
        with open(file_path, "rb") as file:
            upload_response = requests.put(
                signed_url_response.file.url,
                headers=signed_url_response.file.headers,
                data=file,
            )
            if upload_response.status_code != 200:
                raise ValueError(f"Failed to upload file: {upload_response.text}")

        tree_inventory = TreeInventory(
            domain_id=self.domain_id, **signed_url_response.model_dump()
        )

        return tree_inventory


class TreeInventory(TreeInventoryModel):
    """
    A class representing a forest inventory within a spatial domain.

    The TreeInventory class provides access to tree inventory data and operations for a specific
    domain. It supports creating inventories from various data sources (primarily TreeMap),
    monitoring inventory processing status, applying modifications and treatments, and
    exporting data in multiple formats.

    Attributes
    ----------
    domain_id : str
        The unique identifier of the domain this inventory belongs to.
    status : str
        Current processing status of the inventory:
        - "pending": Initial state after creation
        - "running": Being processed
        - "completed": Ready for use
        - "failed": Processing encountered an error
    created_on : datetime
        When the inventory was created.
    modified_on : datetime
        When the inventory was last modified.
    checksum : str
        Unique identifier for this version of the inventory.
    sources : list[str]
        Data sources used to generate the inventory (e.g. ["TreeMap"]).
    tree_map : TreeMapSource, optional
        Configuration used for TreeMap source, if applicable.
    modifications : list[TreeInventoryModification], optional
        Applied modifications to tree attributes.
    treatments : list[TreeInventoryTreatment], optional
        Applied silvicultural treatments.
    feature_masks : list[str], optional
        Applied feature masks (e.g. ["road", "water"]).

    Methods
    -------
    from_domain(domain)
        Retrieve an existing inventory for a domain.
    get(in_place=False)
        Fetch the latest inventory data.
    wait_until_completed(step=5, timeout=600, in_place=True, verbose=False)
        Wait for inventory processing to finish.
    delete()
        Permanently remove this inventory.
    create_export(export_format)
        Create an export of the inventory data.
    get_export(export_format)
        Check status of an existing export.

    Notes
    -----
    - Tree inventories are created using Inventories.create_tree_inventory() or
        Inventories.create_tree_inventory_from_treemap()
    - Processing is asynchronous - use wait_until_completed() to wait for the
      "completed" status
    - Processing time varies with domain size, modifications, and treatments
    - Once completed, inventories can be exported to CSV, Parquet, or GeoJSON formats
    - A domain can only have one tree inventory at a time

    See Also
    --------
    Domain : Spatial container for inventory data
    Inventories : Container for domain inventory resources
    Export : Handles exporting inventory data
    """

    domain_id: str

    @classmethod
    def from_domain_id(cls, domain_id: str) -> TreeInventory:
        """
        Retrieve an existing tree inventory for a domain.

        This method fetches the tree inventory data associated with the provided domain.
        The tree inventory represents a complete forest inventory within the spatial
        context of your domain.

        Parameters
        ----------
        domain_id : str
            The ID of the domain to retrieve the tree inventory for.

        Returns
        -------
        TreeInventory
            A TreeInventory object containing the retrieved inventory data.

        Raises
        ------
        NotFoundException
            If no tree inventory exists for the given domain or if the domain itself
            does not exist.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import TreeInventory
        >>> inventory = TreeInventory.from_domain_id("abc123")
        >>> print(inventory.status)
        'completed'

        Notes
        -----
        - Tree inventories are typically created using Domain.create_tree_inventory() or
          Domain.create_tree_inventory_from_treemap()
        - A domain can only have one tree inventory at a time
        - Use get() to refresh the inventory data and wait_until_completed() to wait
          for processing to finish
        """
        response = _TREE_INVENTORY_API.get_tree_inventory(domain_id=domain_id)
        return cls(domain_id=domain_id, **response.model_dump())

    def get(self, in_place: bool = False):
        """
        Fetch the latest tree inventory data from the API.

        This method retrieves the most recent tree inventory data for the domain,
        allowing you to check the current status and access updated information.
        You can either update the current TreeInventory instance in-place or get
        a new instance with the fresh data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates the current TreeInventory instance with the new data
            and returns self. If False (default), returns a new TreeInventory
            instance with the latest data, leaving the current instance unchanged.

        Returns
        -------
        TreeInventory
            Either the current TreeInventory instance (if in_place=True) or a new
            TreeInventory instance (if in_place=False) containing the latest data.
            Key attributes that may be updated include:
            - status: Current processing status
            - modified_on: Last modification timestamp
            - checksum: Unique identifier for this version
            - sources: Data sources used
            - tree_map: TreeMap configuration
            - modifications: Applied modifications
            - treatments: Applied treatments
            - feature_masks: Applied masks

        Raises
        ------
        NotFoundException
            If the tree inventory or domain no longer exists
        ApiException
            If there is an error communicating with the API

        Examples
        --------
        >>> from fastfuels_sdk import TreeInventory
        >>> inventory = TreeInventory.from_domain_id("abc123")

        Create new instance with latest data:
        >>> updated = inventory.get()  # inventory remains unchanged
        >>> updated is inventory
        False

        Update existing instance in-place:
        >>> inventory.get(in_place=True)  # inventory is updated
        >>> # Any references to inventory now see the updated data

        Notes
        -----
        - The default behavior (in_place=False) ensures immutability by returning
          a new instance. This is safer for concurrent operations but requires
          reassignment if you want to retain the updated data.
        - Use in_place=True when you want to ensure all references to this
          TreeInventory instance see the updated data.
        - This method is often used in conjunction with wait_until_completed()
          to monitor the progress of tree inventory processing.
        """
        response = _TREE_INVENTORY_API.get_tree_inventory(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return TreeInventory(domain_id=self.domain_id, **response.model_dump())

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> TreeInventory:
        """
        Wait for the tree inventory processing to complete.

        Tree inventories are processed asynchronously and may take between several seconds to
        minutes to complete depending on domain size and complexity. This method polls the API at
        regular intervals until the inventory reaches a 'completed' status or the
        timeout is reached.

        Parameters
        ----------
        step : float, optional
            Number of seconds to wait between status checks. Default is 5 seconds.
            Use larger values to reduce API calls, smaller values for more frequent
            updates.

        timeout : float, optional
            Maximum number of seconds to wait for completion. Default is 600 seconds
            (10 minutes). If the timeout is reached before completion, raises a
            TimeoutError.

        in_place : bool, optional
            If True (default), updates the current TreeInventory instance with new data
            at each check. If False, leaves the current instance unchanged and returns
            a new instance when complete.

        verbose : bool, optional
            If True, prints status updates at each check. Default is False.

        Returns
        -------
        TreeInventory
            Either the current TreeInventory instance (if in_place=True) or a new
            TreeInventory instance (if in_place=False) with the completed inventory
            data.

        Raises
        ------
        TimeoutError
            If the tree inventory does not complete within the specified timeout.
        NotFoundException
            If the tree inventory or domain no longer exists.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import TreeInventory
        >>> inventory = TreeInventory.from_domain_id("abc123")

        Basic usage with default parameters:
        >>> completed = inventory.wait_until_completed()
        >>> print(completed.status)
        'completed'

        With progress updates:
        >>> completed = inventory.wait_until_completed(
        ...     step=10,
        ...     timeout=1200,
        ...     verbose=True
        ... )
        Tree inventory has status `pending` (10.00s)
        Tree inventory has status `running` (20.00s)
        Tree inventory has status `completed` (30.00s)

        Without in-place updates:
        >>> completed = inventory.wait_until_completed(in_place=False)
        >>> completed is inventory
        False

        Notes
        -----
        - Processing time varies based on domain size, data sources, modifications,
          and treatments
        - The method polls by calling get() at each interval, which counts against
          API rate limits
        - Consider longer step intervals for large domains or when making many
          API calls
        - For very large domains, you may need to increase the timeout beyond
          the default 10 minutes
        """
        elapsed_time = 0
        tree_inventory = self.get(in_place=in_place if in_place else False)
        while tree_inventory.status != "completed":
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for tree inventory to finish.")
            sleep(step)
            elapsed_time += step
            tree_inventory = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(
                    f"Tree inventory has status `{tree_inventory.status}` ({elapsed_time:.2f}s)"
                )
        return tree_inventory

    def delete(self) -> None:
        """
        Delete this tree inventory.

        Permanently removes the tree inventory from the domain. This action:
        - Deletes the tree inventory data from the database
        - Cancels any ongoing processing jobs
        - Removes associated data from cache and cloud storage
        - Cannot be undone

        Returns
        -------
        None

        Raises
        ------
        NotFoundException
            If the tree inventory or domain no longer exists.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import TreeInventory
        >>> tree_inventory = TreeInventory.from_domain_id("abc123")
        >>> tree_inventory.delete()
        >>> # The inventory is now permanently deleted
        >>> tree_inventory.get()  # This will raise NotFoundException

        Notes
        -----
        - After deletion, any subsequent operations on this TreeInventory instance
          will raise NotFoundException
        - A new tree inventory can be created for the domain after deletion using
          Domain.create_tree_inventory() or Domain.create_tree_inventory_from_treemap()
        - Consider creating an export of important inventory data before deletion
          using create_export()
        """
        _TREE_INVENTORY_API.delete_tree_inventory(domain_id=self.domain_id)

        return None

    def create_export(self, export_format: str) -> Export:
        """
        Create an export of the tree inventory data.

        Initiates an asynchronous process to export the tree inventory data into
        a specified file format. The export process runs in the background and
        generates a downloadable file once complete. Returns an Export object that
        provides methods for monitoring progress and downloading the result.

        Parameters
        ----------
        export_format : str
            The desired format for the exported data. Must be one of:
            - "csv": Comma-separated values format
            - "parquet": Apache Parquet format (efficient for large datasets)
            - "geojson": GeoJSON format (includes spatial information)

        Returns
        -------
        Export
            An Export object for managing the export process.

        Raises
        ------
        ApiException
            If the tree inventory is not in "completed" status or if there is
            an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import TreeInventory
        >>> tree_inventory = TreeInventory.from_domain_id("abc123")

        Basic export with automatic filename:
        >>> tree_inventory.wait_until_completed()
        >>> # Create and wait for export
        >>> export = tree_inventory.create_export("csv")
        >>> export = export.wait_until_completed()
        >>> # Download to current directory
        >>> export.to_file("my/directory")  # Creates 'inventories_tree.csv' in 'my/directory'

        Export with custom filename and progress monitoring:
        >>> export = tree_inventory.create_export("parquet")
        >>> export = export.wait_until_completed(
        ...     step=5,          # Check every 5 seconds
        ...     timeout=300,     # Wait up to 5 minutes
        ... )
        >>> export.to_file("my_trees.parquet")

        Create multiple format exports:
        >>> # Create exports
        >>> csv_export = tree_inventory.create_export("csv")
        >>> parquet_export = tree_inventory.create_export("parquet")
        >>> geojson_export = tree_inventory.create_export("geojson")
        >>> # Wait for all to complete
        >>> for export in [csv_export, parquet_export, geojson_export]:
        ...     export.wait_until_completed(in_place=True)
        >>> # Download to a specific directory
        >>> from pathlib import Path
        >>> output_dir = Path("exports")
        >>> output_dir.mkdir(exist_ok=True)
        >>> for export in [csv_export, parquet_export, geojson_export]:
        ...     export.to_file(output_dir)

        Notes
        -----
        - The tree inventory must be in "completed" status before creating an export
        - Export generation is asynchronous and may take several seconds or minutes depending
          on the data size
        - Each format has specific advantages:
          * CSV: Human-readable, compatible with most software
          * Parquet: Efficient storage and querying for large datasets
          * GeoJSON: Preserves spatial information, works with GIS software
        - The Export object provides methods for monitoring and managing the export
          process - use get() to check status, wait_until_completed() to wait for
          completion, and to_file() to download
        """
        response = _TREE_INVENTORY_API.create_tree_inventory_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def get_export(self, export_format: str) -> Export:
        """
        Retrieve the status of an existing export.

        Fetches the current state of a previously created export in the specified
        format. This method is commonly used to check if an export has completed
        and to get the download URL once it's ready.

        Parameters
        ----------
        export_format : str
            The format of the export to retrieve. Must be one of:
            - "csv": Comma-separated values format
            - "parquet": Apache Parquet format
            - "geojson": GeoJSON format

        Returns
        -------
        Export
            An Export object representing the current state of the export.

        Raises
        ------
        NotFoundException
            If no export exists for the specified format.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import TreeInventory
        >>> tree_inventory = TreeInventory.from_domain_id("abc123")

        Check export status:
        >>> export = tree_inventory.create_export("csv")

        >>> # Check status later
        >>> print(export.status)
        'completed'
        >>> if export.status == "completed":
        ...     export.to_file("trees.csv")

        Monitor export until complete:
        >>> from time import sleep
        >>> export = tree_inventory.create_export("parquet")
        >>> export.wait_until_completed(in_place=True)
        >>> export.to_file("trees.parquet")

        Notes
        -----
        - This method only retrieves status; use create_export() to initiate a new export
        - Export URLs expire after 7 days - you'll need to create a new export after
          expiration
        - The Export object's wait_until_completed() method provides a more
          convenient way to wait for completion
        - If you don't need the intermediate status checks, using
          create_export().wait_until_completed() is simpler
        - Always check the export's status before attempting to download using to_file()
        """
        response = _TREE_INVENTORY_API.get_tree_inventory_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())


def _convert_api_models_to_sdk_classes(domain_id, response_data: dict) -> dict:
    """Convert API models to SDK classes with domain_id."""
    if "tree" in response_data and response_data["tree"]:
        response_data["tree"] = TreeInventory(
            domain_id=domain_id, **response_data["tree"]
        )

    return response_data
