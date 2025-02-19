"""
exports.py
"""

# Core imports
from __future__ import annotations
from time import sleep
from pathlib import Path
from typing import Any
from urllib.request import urlretrieve

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.client_library.models import Export as ExportModel
from fastfuels_sdk.client_library.api import (
    TreeInventoryApi,
    GridsApi,
    TreeGridApi,
    SurfaceGridApi,
    TopographyGridApi,
    FeatureGridApi,
)

# Initialize API clients
_TREE_INVENTORY_API = TreeInventoryApi(get_client())
_GRIDS_API = GridsApi(get_client())
_TREE_GRID_API = TreeGridApi(get_client())
_SURFACE_GRID_API = SurfaceGridApi(get_client())
_TOPOGRAPHY_GRID_API = TopographyGridApi(get_client())
_FEATURE_GRID_API = FeatureGridApi(get_client())

# Define a mapping of (resource, sub_resource) tuples to their corresponding API methods
_API_METHODS = {
    ("inventories", "tree"): _TREE_INVENTORY_API.get_tree_inventory_export,
    ("grids", None): _GRIDS_API.get_grid_export,
    ("grids", "tree"): _TREE_GRID_API.get_tree_grid_export,
    ("grids", "surface"): _SURFACE_GRID_API.get_surface_grid_export,
    ("grids", "topography"): _TOPOGRAPHY_GRID_API.get_topography_grid_export,
    # ("grids", "feature"): _FEATURE_GRID_API.get_feature_grid_export,  # Not yet implemented
}

_FILE_NAMES = {
    ("inventories", "tree", "csv"): "tree_inventory.csv",
    ("inventories", "tree", "parquet"): "tree_inventory.parquet.zip",
    ("inventories", "tree", "geojson"): "tree_inventory.geojson",
    ("grids", None, "QUIC-Fire"): "quicfire.zip",
    ("grids", None, "zarr"): "grid.zarr.zip",
    ("grids", "tree", "zarr"): "tree_grid.zarr.zip",
    ("grids", "surface", "zarr"): "surface_grid.zarr.zip",
    ("grids", "surface", "geotiff"): "surface_grid.tif",
    ("grids", "topography", "zarr"): "topography_grid.zarr.zip",
    ("grids", "topography", "geotiff"): "topography_grid.tif",
}


class Export(ExportModel):
    """
    Class for handling exports of various resources from the FastFuels API.
    Inherits from the base ExportModel and adds functionality for fetching,
    waiting for completion, and downloading exports.

    Attributes
    ----------
    domain_id : str
        The ID of the domain associated with the export
    resource : str
        The type of resource being exported (e.g. "inventories")
    sub_resource : str
        The specific sub-resource being exported (e.g. "tree")
    format : str
        The format of the export (e.g. "csv", "parquet", "geojson")
    status : str
        Current status of the export ("pending", "running", "completed")
    signed_url : str, optional
        URL for downloading the completed export
    _api_get_method : Callable
        The API method to use for getting the export status
    """

    def __init__(self, **data: Any):
        """
        Initialize the Export object and set up the appropriate API method
        based on the resource and sub_resource.

        Parameters
        ----------
        **data : Any
            Keyword arguments that match the ExportModel fields

        Raises
        ------
        NotImplementedError
            If the resource and sub_resource combination is not supported
        """
        super().__init__(**data)

        api_method = _API_METHODS.get((self.resource, self.sub_resource))
        if api_method is None:
            raise NotImplementedError(
                f"Export not implemented for resource={self.resource}, "
                f"sub_resource={self.sub_resource}"
            )

        self._api_get_method = lambda: api_method(
            domain_id=self.domain_id, export_format=self.format
        )

    def get(self, in_place: bool = False) -> Export:
        """
        Fetches the current state of the export from the API.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates the current object with fetched data.
            If False, returns a new Export object. Default is False.

        Returns
        -------
        Export
            Either the current object updated with fresh data (in_place=True)
            or a new Export object with the fetched data (in_place=False)
        """
        response = self._api_get_method()

        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self

        return Export(**response.model_dump())

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> Export:
        """
        Waits for the export to complete, polling at regular intervals.

        Parameters
        ----------
        step : float, optional
            Time in seconds between status checks. Default is 5.
        timeout : float, optional
            Maximum time in seconds to wait for completion. Default is 600.
        in_place : bool, optional
            If True, updates the current object with the completed export data.
            If False, returns a new Export object. Default is True.
        verbose : bool, optional
            If True, prints status updates during the wait. Default is False.

        Returns
        -------
        Export
            The completed export object

        Raises
        ------
        TimeoutError
            If the export does not complete within the specified timeout period.
        """
        elapsed_time = 0
        export = self.get(in_place=in_place if in_place else False)

        while export.status != "completed":
            if elapsed_time >= timeout:
                raise TimeoutError(
                    f"Timed out waiting for export to finish after {timeout} seconds."
                )
            sleep(step)
            elapsed_time += step
            export = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(f"Export has status `{export.status}` ({elapsed_time:.2f}s)")

        return export

    def to_file(self, path: Path | str) -> None:
        """
        Downloads the export to a local file once it's completed.

        Parameters
        ----------
        path : Path or str
            The path where the export should be saved. If a directory is provided,
            the file will be saved as "{resource}_{sub_resource}.{format}" in that directory.

        Raises
        ------
        ValueError
            If the export is not yet completed or if the signed URL is missing
        """
        if isinstance(path, str):
            path = Path(path)

        if path.is_dir():
            path = path / _FILE_NAMES.get(
                (self.resource, self.sub_resource, self.format), "export"
            )

        if self.status != "completed":
            raise ValueError(
                "Export is not yet completed. Please wait for completion before downloading."
            )

        if not self.signed_url:
            raise ValueError(
                "Export does not have a signed URL. Please ensure the export is completed."
            )

        urlretrieve(self.signed_url, path)
