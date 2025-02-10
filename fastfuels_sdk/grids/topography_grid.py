"""
fastfuels_sdk/grids/topography_grid.py
"""

# Core imports
from __future__ import annotations

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.exports import Export
from fastfuels_sdk.client_library.api import TopographyGridApi
from fastfuels_sdk.client_library.models import (
    TopographyGrid as TopographyGridModel,
    GridAttributeMetadataResponse,
)

_TOPOGRAPHY_GRID_API = TopographyGridApi(get_client())


class TopographyGrid(TopographyGridModel):
    """Topography grid data within a domain's spatial boundaries."""

    domain_id: str

    @classmethod
    def from_domain_id(cls, domain_id: str) -> "TopographyGrid":
        """Retrieve an existing topography grid for a domain.

        Parameters
        ----------
        domain_id : str
            ID of the domain to retrieve topography grid for

        Returns
        -------
        TopographyGrid
            The topography grid object

        Examples
        --------
        >>> grid = TopographyGrid.from_domain_id("abc123")
        >>> print(grid.status)
        'completed'
        """
        response = _TOPOGRAPHY_GRID_API.get_topography_grid(domain_id=domain_id)
        return cls(domain_id=domain_id, **response.model_dump())

    def get(self, in_place: bool = False) -> "TopographyGrid":
        """Get the latest topography grid data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this TopographyGrid instance with new data.
            If False (default), returns a new TopographyGrid instance.

        Returns
        -------
        TopographyGrid
            The updated topography grid object

        Examples
        --------
        >>> from fastfuels_sdk import TopographyGrid
        >>> grid = TopographyGrid.from_domain_id("abc123")

        >>> # Get fresh data in a new instance
        >>> updated_grid = grid.get()

        >>> # Or update the existing instance
        >>> grid.get(in_place=True)
        """
        response = _TOPOGRAPHY_GRID_API.get_topography_grid(domain_id=self.domain_id)
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return TopographyGrid(domain_id=self.domain_id, **response.model_dump())

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> "TopographyGrid":
        """Wait for the topography grid processing to complete.

        Topography grids are processed asynchronously and may take between several seconds to
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
            If True (default), updates the current TopographyGrid instance with new data at
            each check. If False, leaves the current instance unchanged and returns a new
            instance when complete.
        verbose : bool, optional
            If True, prints status updates at each check. Default is False.

        Returns
        -------
        TopographyGrid
            Either the current TopographyGrid instance (if in_place=True) or a new
            TopographyGrid instance (if in_place=False) with the completed grid data.

        Raises
        ------
        TimeoutError
            If the topography grid does not complete within the specified timeout.
        NotFoundException
            If the topography grid or domain no longer exists.
        ApiException
            If there is an error communicating with the API.

        Examples
        --------
        >>> from fastfuels_sdk import TopographyGrid
        >>> grid = TopographyGrid.from_domain_id("abc123")

        Basic usage with default parameters:
        >>> completed = grid.wait_until_completed()
        >>> print(completed.status)
        'completed'

        With progress updates:
        >>> completed = grid.wait_until_completed(
        ...     step=10,
        ...     timeout=1200,
        ...     verbose=True
        ... )
        Topography grid has status `pending` (10.00s)
        Topography grid has status `running` (20.00s)
        Topography grid has status `completed` (30.00s)

        Without in-place updates:
        >>> completed = grid.wait_until_completed(in_place=False)
        >>> completed is grid
        False

        Notes
        -----
        - Processing time varies based on domain size and grid configuration
        - The method polls by calling get() at each interval, which counts against API rate limits
        - Consider longer step intervals for large domains or when making many API calls
        - For very large domains, you may need to increase the timeout beyond the default 10 minutes
        """
        from time import sleep

        elapsed_time = 0
        topography_grid = self.get(in_place=in_place if in_place else False)

        while topography_grid.status != "completed":
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for topography grid to finish.")
            sleep(step)
            elapsed_time += step
            topography_grid = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(
                    f"Topography grid has status `{topography_grid.status}` ({elapsed_time:.2f}s)"
                )

        return topography_grid

    def get_attributes(self) -> GridAttributeMetadataResponse:
        """Get metadata about grid attributes.

        Returns metadata about the structure of the topography grid and its attributes,
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
        >>> from fastfuels_sdk import TopographyGrid
        >>> grid = TopographyGrid.from_domain_id("abc123")
        >>> metadata = grid.get_attributes()
        >>> print(metadata.shape)
        [100, 100, 50]
        """
        return _TOPOGRAPHY_GRID_API.get_topography_grid_attribute_metadata(
            domain_id=self.domain_id
        )

    def create_export(self, export_format: str) -> Export:
        """Create an export of the topography grid data.

        Parameters
        ----------
        export_format : str
            Format for the export. Must be one of:
            - "zarr": Compressed array format
            - "geotiff": GeoTIFF format

        Returns
        -------
        Export
            An Export object for managing the export process

        Examples
        --------
        >>> from fastfuels_sdk import TopographyGrid
        >>> grid = TopographyGrid.from_domain_id("abc123")
        >>> export = grid.create_export("zarr")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zarr")
        """
        response = _TOPOGRAPHY_GRID_API.create_topography_grid_export(
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
            - "geotiff": GeoTIFF format

        Returns
        -------
        Export
            An Export object containing current status

        Examples
        --------
        >>> from fastfuels_sdk import TopographyGrid
        >>> grid = TopographyGrid.from_domain_id("abc123")
        >>> export = grid.create_export("zarr")
        >>> export.wait_until_completed()
        >>> export.to_file("grid_data.zarr")
        """
        response = _TOPOGRAPHY_GRID_API.get_topography_grid_export(
            domain_id=self.domain_id, export_format=export_format
        )
        return Export(**response.model_dump())

    def delete(self) -> None:
        """Delete this topography grid.

        Permanently removes topography grid data from the domain. This also cancels
        any ongoing processing jobs.

        Returns
        -------
        None

        Examples
        --------
        >>> from fastfuels_sdk import TopographyGrid
        >>> grid = TopographyGrid.from_domain_id("abc123")
        >>> # Remove grid when no longer needed
        >>> grid.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> grid.get()  # raises NotFoundException
        """
        _TOPOGRAPHY_GRID_API.delete_topography_grid(domain_id=self.domain_id)
        return None
