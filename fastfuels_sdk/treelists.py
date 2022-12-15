"""
Dataset class and endpoints for the FastFuels SDK.
"""

# Internal imports
from fastfuels_sdk import SESSION, API_URL

# Core imports
import json
from pathlib import Path
from datetime import datetime

# External imports
import pandas as pd
from pandas import DataFrame
from requests.exceptions import HTTPError


class Treelist:
    """
    Treelist class for the FastFuels SDK.
    """

    def __init__(self, id: str, name: str, description: str, method: str,
                 dataset_id: str, status: str, created_on: str,
                 summary: dict, fuelgrids: list[str], version: str):
        """
        Initialize a Treelist object.
        """
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.method: str = method
        self.dataset_id: str = dataset_id
        self.status: str = status
        self.created_on: datetime = datetime.fromisoformat(created_on)
        self.summary: dict = summary
        self.fuelgrids: list[str] = fuelgrids
        self.version: str = version


def create_treelist(dataset_id: str, name: str, description: str,
                    method: str = "random") -> Treelist:
    """
    Create a treelist for a dataset.
    """
    # Build the request payload
    payload = json.dumps({
        "dataset_id": dataset_id,
        "name": name,
        "description": description,
        "method": method
    })

    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists"
    response = SESSION.post(endpoint_url, data=payload)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 201:
        raise HTTPError(response.json())

    return Treelist(**response.json())


def get_treelist(treelist_id, units: str = "metric") -> Treelist:
    """
    Get a Treelist object by its ID.

    Parameters
    ----------
    treelist_id : str
        The ID of the Treelist to retrieve.
    units : str, optional
        The units to use for the Treelist summary, by default "metric".
        "imperial" is also supported.

    Returns
    -------
    Treelist
        Treelist object associated with the passed ID at the current time.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    ValueError
        If the passed units are not supported.
    """
    if units not in ["metric", "imperial"]:
        raise ValueError("units must be 'metric' or 'imperial'")

    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists/{treelist_id}?units={units}"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return Treelist(**response.json())


def list_treelists(dataset_id: str = None) -> list[Treelist]:
    """
    List Treelists for a user. Optionally filter by dataset ID.

    Parameters
    ----------
    dataset_id : str, optional
        The ID of the dataset to list Treelists for, by default None.

    Returns
    -------
    list[Treelist]
        List of Treelist objects associated with the passed dataset ID.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    if dataset_id:
        endpoint_url = f"{API_URL}/treelists?dataset_id={dataset_id}"
    else:
        endpoint_url = f"{API_URL}/treelists"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return [Treelist(**treelist) for treelist in response.json()["treelists"]]


def get_treelist_data(treelist_id: str, path: Path) -> Treelist:
    """
    Get a Treelist's data as a CSV file.

    Parameters
    ----------
    treelist_id : str
        The ID of the Treelist to retrieve data for.
    path : Path
        The path to save the CSV file to.

    Returns
    -------
    Treelist
        Treelist object associated with the passed ID at the current time.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists/{treelist_id}/data"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    # Save the CSV file to the passed path
    with open(path, "w") as file:
        file.write(response.text)

    return Treelist(**response.json())


def get_treelist_dataframe(treelist_id: str) -> DataFrame:
    """
    Get a Treelist's data as a Pandas DataFrame.

    Parameters
    ----------
    treelist_id

    Returns
    -------

    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists/{treelist_id}/data"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    # Save the CSV file to the passed path
    return pd.read_csv(response.text)


def update_treelist(treelist_id: str, name: str = None,
                    description: str = None) -> Treelist:
    """
    Update a Treelist resource's name or description.

    Parameters
    ----------
    treelist_id : str
        The ID of the Treelist to update.
    name : str, optional
        The new name for the Treelist, by default None.
    description : str, optional
        The new description for the Treelist, by default None.

    Returns
    -------
    Treelist
        Updated Treelist object.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    ValueError
        If both name and description are None.
    """
    # If both name and description are None, raise an error
    if name is None and description is None:
        raise ValueError("name or description must be provided")

    # Build the request payload
    payload_dict = {}
    if name:
        payload_dict["name"] = name
    if description:
        payload_dict["description"] = description
    payload = json.dumps(payload_dict)

    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists/{treelist_id}"
    response = SESSION.patch(endpoint_url, data=payload)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return Treelist(**response.json())


def update_treelist_data(treelist_id: str) -> Treelist:
    """

    Parameters
    ----------
    treelist_id

    Returns
    -------
    Treelist

    """


def delete_treelist(treelist_id: str, dataset_id: str = None) -> list[Treelist]:
    """
    Delete a Treelist by its ID. Optionally filter remaining treelists by
    dataset ID.

    Parameters
    ----------
    treelist_id : str
        The ID of the Treelist to delete.
    dataset_id : str, optional
        The ID of the dataset to list Treelists for, by default None.

    Returns
    -------
    list[Treelist]
        Remaining Treelist objects. Optionally filtered by dataset ID.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists/{treelist_id}"
    response = SESSION.delete(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return [Treelist(**treelist) for treelist in response.json()["treelists"]]


def delete_all_treelists(dataset_id: str = None) -> list[Treelist]:
    """
    Delete all Treelists for a user. Optionally filter by dataset ID. This is a
    recursive delete that will remove all Fuelgrids associated with each
    Treelist.

    Parameters
    ----------
    dataset_id : str, optional
        The ID of the dataset to list Treelists for, by default None.

    Returns
    -------
    list[Treelist]
        Remaining Treelist objects. Optionally filtered by dataset ID.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    if dataset_id:
        endpoint_url = f"{API_URL}/treelists?dataset_id={dataset_id}"
    else:
        endpoint_url = f"{API_URL}/treelists"
    response = SESSION.delete(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return [Treelist(**treelist) for treelist in response.json()["treelists"]]
