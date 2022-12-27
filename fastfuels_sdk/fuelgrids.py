"""
Fuelgrid class and endpoints for the FastFuels SDK.
"""

# Internal imports
from fastfuels_sdk import SESSION, API_URL

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

    def __init__(self, id: str, dataset_id: str, treelist_id: str, name: str,
                 description: str, surface_fuel_source: str,
                 surface_interpolation_method: str, distribution_method: str,
                 horizontal_resolution: float, vertical_resolution: float,
                 border_pad: float, status: str, created_on: str, version: str):
        """
        Initialize a Fuelgrid object.
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


def create_fuelgrid(dataset_id: str, treelist_id: str, name: str,
                    description: str, distribution_method: str,
                    horizontal_resolution: float, vertical_resolution: float,
                    border_pad: float, surface_fuel_source: str = "LF_SB40",
                    surface_interpolation_method: str = "nearest") -> Fuelgrid:
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
    surface_fuel_source : str
        The source of the surface fuel data. Only "LF_SB40" is currently
        supported. Defaults to "LF_SB40".
    surface_interpolation_method : str
        The interpolation method to use for surface fuel data. "nearest",
        "zipper", "linear", and "cubic" are supported. Defaults to "nearest".
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


# TODO: Add a parameter to get all fuelgrids for a dataset
# TODO: Add a parameter to get all fuelgrids for a treelist
def list_fuelgrids() -> list[Fuelgrid]:
    """
    List all fuelgrids.

    Returns
    -------
    list[Fuelgrid]
        List of fuelgrids.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.

    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids"
    response = SESSION.get(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return [Fuelgrid(**fuelgrid) for fuelgrid in response.json()["fuelgrids"]]


def download_fuelgrid_data(fuelgrid_id: str, fpath: Path | str) -> None:
    """
    Stream fuel grid 3D array data to a binary zarr file

    Parameters
    ----------
    fuelgrid_id
    fpath

    Returns
    -------

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


# TODO: Add a parameter to delete all fuelgrids for a dataset
# TODO: Add a parameter to delete all fuelgrids for a treelist
def delete_all_fuelgrids():
    """
    Delete all fuelgrids.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/fuelgrids"
    response = SESSION.delete(endpoint_url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        raise HTTPError(f"Request to {endpoint_url} failed with status code "
                        f"{response.status_code}. Response: {response.json()}")

    return [Fuelgrid(**fuelgrid) for fuelgrid in response.json()["fuelgrids"]]


