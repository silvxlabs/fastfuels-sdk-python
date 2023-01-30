"""
Fuelgrid class and endpoints for the FastFuels SDK.
"""

# Internal imports
from fastfuels_sdk.api import SESSION, API_URL

# Core imports
import json
import shutil
from pathlib import Path
from datetime import datetime

# External imports
from requests.exceptions import HTTPError


class Fuelgrid:
    """
    Fuelgrid class for the FastFuels SDK.
    """

    def __init__(self, id: str, dataset_id: str, treelist_id: str,
                 name: str, description: str, surface_fuel_source: str,
                 surface_interpolation_method: str, distribution_method: str,
                 horizontal_resolution: float, vertical_resolution: float,
                 border_pad: float, status: str, created_on: str, version: str):
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
               inplace: bool = False) -> None:
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
        None

        Raises
        ------
        HTTPError
            If the API returns an unsuccessful status code.
        """
        # update_fuelgrid(self.id, name, description)

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
                    description: str, distribution_method: str,
                    horizontal_resolution: float, vertical_resolution: float,
                    border_pad: float, surface_fuel_source: str = "LF_SB40",
                    surface_interpolation_method: str = "nearest") -> Fuelgrid:
    """
    Create a fuelgrid by voxelizing a treelist.

    Parameters
    ----------
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
        "border_pad": border_pad
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


# TODO: Add a parameter to delete all fuelgrids for a dataset
# TODO: Add a parameter to delete all fuelgrids for a treelist
def delete_all_fuelgrids(dataset_id: str = None,
                         treelist_id: str = None) -> list[Fuelgrid]:
    """
    Delete all fuelgrids.

    Parameters
    ----------
    dataset_id : str, optional
        The ID of the dataset to filter by, by default None
    treelist_id : str, optional
        The ID of the treelist to filter by, by default None

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
    endpoint_url = f"{API_URL}/fuelgrids"
    response = SESSION.delete(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return [Fuelgrid(**fuelgrid) for fuelgrid in response.json()["fuelgrids"]]
