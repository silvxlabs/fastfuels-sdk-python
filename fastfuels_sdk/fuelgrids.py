"""
Fuelgrid class and endpoints for the FastFuels SDK.
"""
# Core imports
from __future__ import annotations
import json
import shutil
from time import sleep
from pathlib import Path
from datetime import datetime

# Internal imports
from fastfuels_sdk.api import SESSION, API_URL
from fastfuels_sdk._base import FastFuelsResource

# External imports
from requests.exceptions import HTTPError


class Fuelgrid(FastFuelsResource):
    """
    Fuelgrid class for the FastFuels SDK.
    """

    def __init__(self, id: str, dataset_id: str, treelist_id: str,
                 name: str, description: str, surface_fuel_source: str,
                 surface_interpolation_method: str, distribution_method: str,
                 horizontal_resolution: float, vertical_resolution: float,
                 border_pad: float, status: str, created_on: str, version: str,
                 outputs: dict):
        """
        Initialize a Fuelgrid object.

        Parameters
        ----------
        id : str
            The unique identifier for the fuelgrid.
        dataset_id : str
            The unique identifier for the dataset used to create the fuelgrid.
        treelist_id : str
            The unique identifier for the treelist used to create the fuelgrid.
        name : str
            The name of the fuelgrid.
        description : str
            The description of the fuelgrid.
        surface_fuel_source : str
            The surface fuel source used to create the fuelgrid.
        surface_interpolation_method : str
            The surface interpolation method used to create the fuelgrid.
        distribution_method : str
            The distribution method used to create the fuelgrid.
        horizontal_resolution : float
            The horizontal resolution of the fuelgrid.
        vertical_resolution : float
            The vertical resolution of the fuelgrid.
        border_pad : float
            The border pad of the fuelgrid.
        status : str
            The status of the fuelgrid.
        created_on : str
            The date and time the fuelgrid was created. The data is read in ISO
            8601 format and converted to a datetime object.
        version : str
            The version of treevox used to generate the fuelgrid.
        outputs : dict
            The outputs of the fuelgrid.
        """
        self.id: str = id
        self.dataset_id: str = dataset_id
        self.treelist_id: str = treelist_id
        self.name: str = name
        self.description: str = description
        self.surface_fuel_source: str = surface_fuel_source
        self.surface_interpolation_method: str = surface_interpolation_method
        self.distribution_method: str = distribution_method
        self.horizontal_resolution: float = horizontal_resolution
        self.vertical_resolution: float = vertical_resolution
        self.border_pad: float = border_pad
        self.status: str = status
        self.created_on: datetime = datetime.fromisoformat(created_on)
        self.version: str = version
        self.outputs: dict = outputs

    def refresh(self, inplace: bool = False) -> Fuelgrid | None:
        """
        Refresh the Fuelgrid object with the latest data from the server.

        Parameters
        ----------
        inplace : bool, optional
            Whether to update the Fuelgrid object in place, or return a new
            Fuelgrid object, by default False

        Returns
        -------
        Fuelgrid | None
            A new Fuelgrid object if inplace is False, otherwise None.
        """
        fuelgrid = get_fuelgrid(self.id)
        if inplace:
            self.__dict__ = fuelgrid.__dict__
        else:
            return fuelgrid

    def wait_until_finished(self, step: float = 5, timeout: float = 600,
                            inplace: bool = False,
                            verbose: bool = False) -> Fuelgrid | None:
        """
        Wait until the fuelgrid resource is finished.

        Parameters
        ----------
        step : float, optional
            The time in seconds to wait between checking the status of the
            Fuelgrid, by default 5 seconds.
        timeout : float, optional
            The time in seconds to wait before raising a TimeoutError, by
            default 600 seconds (10 minutes). Note that the timeout is
            different from the timeout used in the API. Just because the
            timeout is reached here does not mean that the Fuelgrid resource has
            failed.
        inplace : bool, optional
            Whether to update the Fuelgrid object in place, or return a new
            fuelgrid object. By default, False.
        verbose : bool, optional
            Whether to print the status of the Fuelgrid, by default False.

        Returns
        -------
        Fuelgrid | None
            If inplace is False, returns a new Fuelgrid object. Otherwise,
            returns None and updates the existing fuelgrid object in place.
        """
        elapsed_time = 0
        fuelgrid = get_fuelgrid(self.id)
        while fuelgrid.status != "Finished":
            if fuelgrid.status == "Failed":
                raise RuntimeError(f"Fuelgrid {fuelgrid.name} has status "
                                   f"'Failed'.")
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for fuelgrid to finish.")
            sleep(step)
            elapsed_time += step
            fuelgrid = get_fuelgrid(self.id)
            if verbose:
                print(f"Fuelgrid {fuelgrid.name}: {fuelgrid.status} "
                      f"({elapsed_time:.2f}s)")

        if inplace:
            self.__dict__ = fuelgrid.__dict__
        else:
            return fuelgrid

    def download_zarr(self, fpath: Path | str) -> None:
        """
        Stream fuel grid 3D array data to a binary zarr file

        Parameters
        ----------
        fpath

        Returns
        -------
        None
            File is saved to disk.

        Raises
        ------
        HTTPError
            If the API returns an unsuccessful status code.
        """
        download_zarr(self.id, fpath)

    def update(self, name: str = None, description: str = None,
               inplace: bool = False) -> Fuelgrid | None:
        """
        Update the name and description of the fuelgrid.

        Parameters
        ----------
        name : str
            The new name of the fuelgrid.
        description : str
            The new description of the fuelgrid.
        inplace : bool
            If True, the fuelgrid object is updated in place. If False, a new
            fuelgrid object is returned. Default is False.

        Returns
        -------
        Fuelgrid | None
            If inplace is False, returns a new Fuelgrid object. Otherwise,
            returns None and updates the existing fuelgrid object in place.

        Raises
        ------
        HTTPError
            If the API returns an unsuccessful status code.
        """
        updated_fuelgrid = update_fuelgrid(self.id, name, description)
        if inplace:
            self.__dict__ = updated_fuelgrid.__dict__
        else:
            return updated_fuelgrid

    def delete(self) -> None:
        """
        Delete the fuelgrid.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If the API returns an unsuccessful status code.
        """
        delete_fuelgrid(self.id)


def create_fuelgrid(dataset_id: str, treelist_id: str, name: str,
                    description: str = "", distribution_method: str = "uniform",
                    horizontal_resolution: float = 1,
                    vertical_resolution: float = 1,
                    border_pad: float = 0, surface_fuel_source: str = "LF_SB40",
                    surface_interpolation_method: str = "nearest",
                    write_sparse_array: bool = False) -> Fuelgrid:
    """
    Create a fuelgrid by voxelizing a treelist.

    Parameters
    ----------
    dataset_id : str
        The ID of the dataset to use.
    treelist_id : str
        The ID of the treelist to use.
    name : str
        The name of the fuelgrid.
    description : str
        The description of the fuelgrid.
    distribution_method : str
        The method to use for distributing fuel data. "uniform", "random", and
        "realistic" are currently supported.
    horizontal_resolution : float
        The horizontal resolution of the fuelgrid in meters.
    vertical_resolution : float
        The vertical resolution of the fuelgrid in meters.
    border_pad : float
        The amount of padding to add to the border of the fuelgrid in meters.
        Voxelized trees that intersect with the border of the domain can be
        cut off if the entire canopy is not included in the domain. This extra
        padding can ensure that the entire canopy is included in the domain.
    surface_fuel_source : str
        The source of the surface fuel data. Only "LF_SB40" is currently
        supported. Defaults to "LF_SB40".
    surface_interpolation_method : str
        The interpolation method to use for surface fuel data. "nearest",
        "zipper", "linear", and "cubic" are supported. Defaults to "nearest".
    write_sparse_array : bool
        If True, a sparse fuel grid array will be written to disk. This is in
        addition to the zarr file. Defaults to False. This is useful for
        linking the fuelgrid to treelist data for fire effects modeling. The
        sparse array is a 3D array with the same dimensions as the zarr file.
        Writing the sparse array can take a long time and is not recommended
        for large fuel grids.

    Returns
    -------
    Fuelgrid
        Voxelized treelist.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    ValueError
        If surface_fuel_source is not "LF_SB40".
    ValueError
        If surface_interpolation_method is not "nearest", "zipper", "linear",
        or "cubic".
    ValueError
        If distribution_method is not "uniform", "random", or "realistic".

    Notes
    -----
    There is a slight discrepancy between the spatial extent of the fuelgrid and
    the spatial extent of the Dataset. The fuelgrid spatial extent rounded out
    to the nearest multiple of the horizontal resolution. This ensures that all
    grid cells are a uniform size specified by the horizontal resolution.

    Individual trees may extend beyond the Fuelgrid spatial extent. If this is
    the case the canopy of the tree will be cut off at the edge of the
    Fuelgrid. This can be avoided by increasing the border_pad.

    """
    # Check for valid inputs
    if surface_fuel_source != "LF_SB40":
        raise ValueError("surface_fuel_source must be 'LF_SB40'")
    if surface_interpolation_method not in ["nearest", "zipper", "linear",
                                            "cubic"]:
        raise ValueError(
            "surface_interpolation_method must be 'nearest', 'zipper', "
            "'linear', or 'cubic'")
    if distribution_method not in ["uniform", "random", "realistic"]:
        raise ValueError(
            "distribution_method must be 'uniform', 'random', or 'realistic'")

    # Create the payload
    payload_dict = {
        "dataset_id": dataset_id,
        "treelist_id": treelist_id,
        "name": name,
        "description": description,
        "surface_fuel_source": surface_fuel_source,
        "surface_interpolation_method": surface_interpolation_method,
        "distribution_method": distribution_method,
        "horizontal_resolution": horizontal_resolution,
        "vertical_resolution": vertical_resolution,
        "border_pad": border_pad,
        "outputs": {
            "sparse_array": write_sparse_array,
        }
    }
    payload = json.dumps(payload_dict)

    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids"
    response = SESSION.post(endpoint_url, data=payload)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 201:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return Fuelgrid(**response.json())


def get_fuelgrid(fuelgrid_id: str) -> Fuelgrid:
    """
    Get a fuelgrid by ID.

    Parameters
    ----------
    fuelgrid_id : str
        The ID of the fuelgrid to get.

    Returns
    -------
    Fuelgrid
        The fuelgrid.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids/{fuelgrid_id}"
    response = SESSION.get(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return Fuelgrid(**response.json())


def list_fuelgrids(dataset_id: str = None,
                   treelist_id: str = None) -> list[Fuelgrid]:
    """
    List all fuelgrids.

    Parameters
    ----------
    dataset_id : str, optional
        The ID of the dataset to filter by, by default None
    treelist_id : str, optional
        The ID of the treelist to filter by, by default None

    Returns
    -------
    list[Fuelgrid]
        List of fuelgrids.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Filter by dataset or treelist if specified
    if dataset_id is not None:
        endpoint_url = f"{API_URL}/fuelgrids?dataset_id={dataset_id}"
    elif treelist_id is not None:
        endpoint_url = f"{API_URL}/fuelgrids?treelist_id={treelist_id}"
    else:
        endpoint_url = f"{API_URL}/fuelgrids"

    # Send the request to the API
    response = SESSION.get(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return [Fuelgrid(**fuelgrid) for fuelgrid in response.json()["fuelgrids"]]


def download_zarr(fuelgrid_id: str, fpath: Path | str) -> None:
    """
    Stream fuel grid 3D array data to a binary zarr file

    Parameters
    ----------
    fuelgrid_id
    fpath

    Returns
    -------
    None
        File is saved to disk.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # If fpath is a string, convert it to a Path
    if isinstance(fpath, str):
        fpath = Path(fpath)

    # If fpath is a directory, create a file name
    if fpath.is_dir():
        fuelgrid = get_fuelgrid(fuelgrid_id)
        fpath = Path(fpath, f"{fuelgrid.name}.zip")

    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids/{fuelgrid_id}/data?fmt=zarr"
    response = SESSION.get(endpoint_url, stream=True)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    # Write the streamed response to a file
    with open(fpath, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)


def update_fuelgrid(fuelgrid_id: str, name: str = None,
                    description: str = None) -> Fuelgrid:
    """
    Update a fuelgrid by ID.

    Parameters
    ----------
    fuelgrid_id : str
        The ID of the fuelgrid to update.
    name : str, optional
        The new name of the fuelgrid.
    description : str, optional
        The new description of the fuelgrid.

    Returns
    -------
    Fuelgrid
        The updated fuelgrid.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Build the request payload
    payload = {}
    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description

    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids/{fuelgrid_id}"
    response = SESSION.put(endpoint_url, json=payload)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return Fuelgrid(**response.json())


def delete_fuelgrid(fuelgrid_id: str) -> list[Fuelgrid]:
    """
    Delete a fuelgrid by ID.

    Parameters
    ----------
    fuelgrid_id: str
        The ID of the fuelgrid to delete.

    Returns
    -------
    list[Fuelgrid]
        Remaining fuelgrids.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids/{fuelgrid_id}"
    response = SESSION.delete(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return [Fuelgrid(**fuelgrid) for fuelgrid in response.json()["fuelgrids"]]


def delete_all_fuelgrids(dataset_id: str = None,
                         treelist_id: str = None) -> list[Fuelgrid]:
    """
    Delete all fuelgrids associated with a specified dataset or treelist.

    Parameters
    ----------
    dataset_id : str, optional
        The ID of the dataset whose associated fuelgrids are to be deleted, by
        default None
    treelist_id : str, optional
        The ID of the treelist whose associated fuelgrids are to be deleted,
        by default None

    Returns
    -------
    list[Fuelgrid]
        Remaining fuelgrids.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.

    Notes
    -----
    If both dataset_id and treelist_id are provided, the function will use the
    dataset_id as the query parameter.

    """
    # Construct the endpoint URL
    if dataset_id is not None:
        endpoint_url = f"{API_URL}/fuelgrids?dataset_id={dataset_id}"
    elif treelist_id is not None:
        endpoint_url = f"{API_URL}/fuelgrids?treelist_id={treelist_id}"
    else:
        endpoint_url = f"{API_URL}/fuelgrids"

    # Send the request to the API
    response = SESSION.delete(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return [Fuelgrid(**fuelgrid) for fuelgrid in response.json()["fuelgrids"]]
