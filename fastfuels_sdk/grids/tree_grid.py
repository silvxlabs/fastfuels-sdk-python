"""
fastfuels_sdk/grids/tree_grid.py
"""

# Core imports
from __future__ import annotations

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.exports import Export
from fastfuels_sdk.client_library.api import TreeGridApi
from fastfuels_sdk.client_library.models import (
    TreeGrid as TreeGridModel,
    GridAttributeMetadataResponse,
)

_TREE_GRID_API = TreeGridApi(get_client())


class TreeGrid(TreeGridModel):
    """Tree grid data within a domain's spatial boundaries."""

    domain_id: str

    @classmethod
    def from_domain_id(cls, domain_id: str) -> TreeGrid:
        """Retrieve an existing tree grid for a domain.

        Parameters
        ----------
        domain_id : str
            ID of the domain to retrieve tree grid for

        Returns
        -------
        TreeGrid
            The tree grid object

        Examples
        --------
        >>> tree_grid = TreeGrid.from_domain_id("abc123")
        >>> tree_grid.status
        'completed'
        """
        response = _TREE_GRID_API.get_tree_grid(domain_id=domain_id)
        return cls(domain_id=domain_id, **response.model_dump())

    def get(self, in_place: bool = False) -> TreeGrid:
        """Get the latest tree grid data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this TreeGrid instance with new data.
            If False (default), returns a new TreeGrid instance.

        Returns
        -------
        TreeGrid
            The updated tree grid object

        Examples
        --------
        >>> from fastfuels_sdk import TreeGrid
        >>> tree_grid = TreeGrid.from_domain_id("abc123")
        >>>
        >>> # Get fresh data in a new instance
        >>> updated_grid = tree_grid.get()
        >>>
        >>> # Or update the existing instance
        >>> tree_grid.get(in_place=True)
        """
        response = _TREE_GRID_API.get_tree_grid(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return TreeGrid(domain_id=self.domain_id, **response.model_dump())

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> "TreeGrid":
        """Wait for the tree grid processing to complete.

        Tree grids are processed asynchronously and may take between several seconds to
        minutes to complete depending on domain size and complexity. This method polls the API at
        regular intervals until the grid reaches a 'completed' status or the timeout is reached.

        Parameters
        ----------
        step : float, optional
            Number of seconds to wait between status checks. Default is 5 seconds.
            Use larger values to reduce API calls, smaller values for more frequent updates.
        timeout : float, optional
            Maximum number of seconds to wait for completion. Default is 600 seconds
            (10 minutes). If the timeout is reached before completion, raises a TimeoutError.
        in_place : bool, optional
            If True (default), updates the current TreeGrid instance with new data at
            each check. If False, leaves the current instance unchanged and returns a new
            instance when complete.
        verbose : bool, optional
            If True, prints status updates at each check. Default is False.

        Returns
        -------
        TreeGrid
            Either the current TreeGrid instance (if in_place=True) or a new
            TreeGrid instance (if in_place=False) with the completed grid data.

        Raises
        ------
        TimeoutError
            If the tree grid does not complete within the specified timeout.
        NotFoundException
            If the tree grid or domain no longer exists.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        Basic usage with default parameters:
        from fastfuels_sdk import TreeGrid
        >>> grid = TreeGrid.from_domain_id("abc123")
        >>> completed = grid.wait_until_completed()
        >>> print(completed.status)
        'completed'

        With progress updates:
        >>> completed = grid.wait_until_completed(
        ...     step=10,
        ...     timeout=1200,
        ...     verbose=True
        ... )
        Tree grid has status `pending` (10.00s)
        Tree grid has status `running` (20.00s)
        Tree grid has status `completed` (30.00s)
        """
        from time import sleep

        elapsed_time = 0
        tree_grid = self.get(in_place=in_place if in_place else False)

        while tree_grid.status != "completed":
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for tree grid to finish.")
            sleep(step)
            elapsed_time += step
            tree_grid = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(
                    f"Tree grid has status `{tree_grid.status}` ({elapsed_time:.2f}s)"
                )

        return tree_grid

    def get_attributes(self) -> GridAttributeMetadataResponse:
        """Get metadata about grid attributes.

        Returns metadata about the structure of the tree grid and its attributes,
        including dimensions, chunking, and attribute details.

        Returns
        -------
        GridAttributeMetadataResponse
            Metadata about grid structure and attributes including:
            - shape: Dimensions of the grid data
            - dimensions: Names of each dimension
            - chunks: Number of chunks in each dimension
            - chunk_shape: Shape of each chunk
            - attributes: Detailed information about each attribute

        Examples
        --------
        >>> from fastfuels_sdk import TreeGrid
        >>> tree_grid = TreeGrid.from_domain_id("abc123")
        >>> metadata = tree_grid.get_attributes()
        >>> print(metadata.shape)
        [100, 100, 50]
        """
        return _TREE_GRID_API.get_tree_grid_attribute_metadata(domain_id=self.domain_id)

    def create_export(self, export_format: str) -> Export:
        """Create an export of the tree grid data.

        Parameters
        ----------
        export_format : str
            Format for the export. Must be one of:
            - "zarr": Compressed array format

        Returns
        -------
        Export
            An Export object for managing the export process


        Examples
        --------
        >>> from fastfuels_sdk import TreeGrid
        >>> tree_grid = TreeGrid.from_domain_id("abc123")
        >>> export = tree_grid.create_export("zarr")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zarr")
        """
        response = _TREE_GRID_API.create_tree_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def get_export(self, export_format: str) -> Export:
        """Get the status of an existing export.

        Parameters
        ----------
        export_format : str
            Format of the export to check. Must be one of:
            - "zarr": Compressed array format

        Returns
        -------
        Export
            An Export object containing current status

        Examples
        --------
        >>> from fastfuels_sdk import TreeGrid
        >>> tree_grid = TreeGrid.from_domain_id("abc123")
        >>> export = tree_grid.create_export("zarr")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zarr")
        """
        response = _TREE_GRID_API.get_tree_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def delete(self) -> None:
        """Delete this tree grid.

        Permanently removes tree grid data from the domain. This also cancels
        any ongoing processing jobs.

        Returns
        -------
        None

        Examples
        --------
        >>> from fastfuels_sdk import TreeGrid
        >>> tree_grid = TreeGrid.from_domain_id("abc123")
        >>> # Remove grid when no longer needed
        >>> tree_grid.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> tree_grid.get()  # raises NotFoundException
        """
        _TREE_GRID_API.delete_tree_grid(domain_id=self.domain_id)
        return None
