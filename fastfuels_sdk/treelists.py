"""
Treelist class and endpoints for the FastFuels SDK.
"""

# Internal imports
from fastfuels_sdk.api import SESSION, API_URL
from fastfuels_sdk.fuelgrids import (Fuelgrid, create_fuelgrid, list_fuelgrids,
                                     delete_all_fuelgrids)

# Core imports
import json
import tempfile
from pathlib import Path
from datetime import datetime

# External imports
import pandas as pd
from pandas import DataFrame
from requests.exceptions import HTTPError


class Treelist:
    """
    # TODO #5: Explain what a treelist is.
    Treelist class for the FastFuels SDK.

    # TODO #5: Add Attributes section.
    # TODO #5: Add Methods section.
    """

    def __init__(self, treelist_id: str, name: str, description: str, method: str,
                 dataset_id: str, status: str, created_on: str,
                 summary: dict, fuelgrids: list[str], version: str):
        """
        Initialize a Treelist object.

        Parameters
        ----------
        treelist_id : str
            The unique identifier of the treelist.
        name : str
            The name of the treelist.
        description : str
            The description of the treelist.
        method : str
            Method used to distribute trees on the landscape.
        dataset_id : str
            The unique identifier of the dataset the treelist belongs to.
        status : str
            Status of the treelist at the time of the request. Note that the
            status of a treelist can change after the request.
        created_on : str
            The date and time the treelist was created. The data is read in
            ISO 8601 format and converted to a datetime object.
        summary : dict
            A dictionary containing summary statistics for the treelist.
        fuelgrids : list[str]
            A list of the IDs of the fuelgrids created from the treelist.
        version : str
            The version of standgen used to generate the treelist.
        """
        self.id: str = treelist_id
        self.name: str = name
        self.description: str = description
        self.method: str = method
        self.dataset_id: str = dataset_id
        self.status: str = status
        self.created_on: datetime = datetime.fromisoformat(created_on)
        self.summary: dict = summary
        self.fuelgrids: list[str] = fuelgrids
        self.version: str = version

    def get_data(self) -> DataFrame:
        """
        # TODO #5: Explain what data is included in the DataFrame. Can reference the get_treelist_data() docstring.
        Returns the treelist data as a pandas DataFrame.


        Returns
        -------
        DataFrame
            A pandas DataFrame containing the treelist data.

        # TODO #5: Add Raises, Notes, and Examples sections.
        """
        return get_treelist_data(self.id)

    def update(self, name: str = None, description: str = None,
               inplace: bool = False):
        """
        Update a treelist resource. The attributes that can be updated are name
        and description.

        If inplace is True, the current Treelist object will be updated with the
        new values. Otherwise, a new Treelist object will be returned.

        Parameters
        ----------
        name : str, optional
            Name of the treelist to update, by default None.
        description : str, optional
            Description of the treelist to update, by default None.
        inplace : bool, optional
            Whether to update the treelist object in place, or return a new
            treelist object. By default False.

        Returns
        -------
        Treelist
            Updated Treelist object.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        updated_treelist = update_treelist(self.id, name, description)
        if inplace:
            self.__dict__.update(updated_treelist.__dict__)
        else:
            return updated_treelist

    def update_data(self, data: DataFrame, inplace: bool = False):
        # """
        # Allows a user to upload a custom .csv or .parquet file to update an
        # existing treelist resource. Note that trees outside the spatial bounding
        # box of the dataset will be removed.
        #
        # The custom treelist data must contain the following columns:
        #  - 'SPCD'
        #  - 'DIA_cm'
        #  - 'HT_m'
        #  - 'STATUSCD'
        #  - 'CBH_m'
        #  - 'X_m',
        #  - 'Y_m'
        #
        # The following columns are optional, and if present, will replace default
        # values during the voxelization process:
        #  - 'FOLIAGE_WEIGHT_kg'
        #  - 'CROWN_VOLUME_m3'
        #  - 'CROWN_RADIUS_m'
        #
        # Parameters
        # ----------
        # data: DataFrame
        #     A Pandas DataFrame containing the custom treelist data.
        # inplace : bool, optional
        #     Whether to update the treelist object in place, or return a new
        #     treelist object. By default False.
        #
        # Returns
        # -------
        # Treelist
        #     Updated Treelist object.
        # """
        updated_treelist = update_treelist_data(self.id, data)
        if inplace:
            self.__dict__.update(updated_treelist.__dict__)
        else:
            return updated_treelist

    def create_fuelgrid(self, name: str, description: str,
                        distribution_method: str, horizontal_resolution: float,
                        vertical_resolution: float, border_pad: float,
                        surface_fuel_source: str = "LF_SB40",
                        surface_interpolation_method: str = "nearest") -> Fuelgrid:
        """
        # TODO #5: Explain what a fuelgrid is. Can copy from, or link to, the fuelgrid docstring
        Create a fuelgrid from a treelist.

        Parameters
        ----------
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
            A Fuelgrid object.

        Raises
        ------
        HTTPError
            If the API returns an unsuccessful status code.
        ValueError
            If surface_fuel_source is not "LF_SB40".
        ValueError
            If surface_interpolation_method is not "nearest", "zipper", "linear"
            , or "cubic".
        ValueError
            If distribution_method is not "uniform", "random", or "realistic".

        """
        return create_fuelgrid(self.dataset_id, self.id, name,
                               description, distribution_method,
                               horizontal_resolution, vertical_resolution,
                               border_pad, surface_fuel_source,
                               surface_interpolation_method)

    # TODO: Write a method to list fuelgrids associated with a dataset
    def list_fuelgrids(self):
        pass

    # TODO: Write a method to delete fuelgrids associated with a treelist
    def delete_fuelsgrids(self):
        pass

    def delete(self):
        """
        Delete a treelist resource.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        delete_treelist(self.id)


def create_treelist(dataset_id: str, name: str, description: str,
                    method: str = "random") -> Treelist:
    """
    Create a Treelist from the spatial bounding box of a Dataset. Note that a
    Treelist resource contains metadata about the Treelist and associated
    Fuelgrid resources. Treelist data refers to the actual tree data stored
    in a table format.

    Once a Treelist resource is created and enters the "Finished"
    status, the data can be accessed as a Pandas DataFrame through the
    get_treelist_data() method.

    Parameters
    ----------
    dataset_id : str
        The ID of the Dataset to create the Treelist for. The Dataset provides
        the spatial bounding box for the Treelist.
    name : str
        The name of the treelist.
    description : str
        The description of the treelist.
    method : str, optional
        The method to use for generating the treelist. Defaults to "random".
        Currently only "random" is supported.
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

    # Rename the "id" key to "treelist_id" for object instantiation
    response_dict = response.json()
    response_dict["treelist_id"] = response_dict.pop("id")

    return Treelist(**response_dict)


def get_treelist(treelist_id, units: str = "metric") -> Treelist:
    """
    Returns a Treelist object populated with resource data from the API for
    the specified treelist ID.

    Summary statistics for the treelist data are also returned with either
    metric or imperial units. All summary statistics are presented on a
    per-area basis. If units are metric (default), the area is in hectares. If
    units are imperial, the area is in acres. Only live trees are included in
    the summary values.

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
    List Treelist objects for a user. Optionally, filter Treelists by
    dataset ID. By default, all Treelists are returned.

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


def get_treelist_data(treelist_id: str) -> DataFrame:
    """
    Returns Treelist data as a Pandas DataFrame.

    Treelist data is stored in a table format. Each row represents a tree
    and each column represents a tree attribute. The columns are:
    - SPCD: FIA Species code
    - DIA_cm: Tree diameter at breast height (centimeters)
    - HT_m: Tree height (meters)
    - STATUSCD: FIA Status code
    - CBH_m: Tree crown base height (meters)
    - X_m: Tree X coordinate in EPSG:5070 (meters)
    - Y_m: Tree Y coordinate in EPSG:5070 (meters)

    Parameters
    ----------
    treelist_id: str
        The ID of the Treelist to retrieve data for.

    Returns
    -------
    DataFrame
        Pandas DataFrame containing the treelist data.

    Raises
    ------
    HTTPError
        If the API returns an unsuccessful status code.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/treelists/{treelist_id}/data?fmt=csv"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    # Write the response to a temporary file
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(response.content)
        temp_file.seek(0)
        df = pd.read_csv(temp_file.name)

    return df


def update_treelist(treelist_id: str, name: str = None,
                    description: str = None) -> Treelist:
    """
    Update a Treelist resource. The attributes that can be updated are the name
    and description.

    This endpoint will not modify the Treelist data. To
    upload new Treelist data see the upload_treelist_data() method.

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


def update_treelist_data(treelist_id: str, data: DataFrame) -> Treelist:
    """
    Allows a user to upload a custom .csv or .parquet file to update an existing
    treelist resource. Trees outside the spatial bounding box of the dataset
    will be removed.

    The custom treelist data must contain the following columns:
    - 'SPCD'
    - 'DIA_cm'
    - 'HT_m'
    - 'STATUSCD'
    - 'CBH_m'
    - 'X_m',
    - 'Y_m'

    The following columns are optional, and will replace the values from default
    allometric equations during the voxelization process:
     - 'FOLIAGE_WEIGHT_kg'
     - 'CROWN_VOLUME_m3'
     - 'CROWN_RADIUS_m'

    Parameters
    ----------
    treelist_id: str
        The ID of the Treelist to update.
    data: DataFrame
        A Pandas DataFrame containing the custom treelist data.

    Returns
    -------
    Treelist
        Updated Treelist resource with the updated data.
    """
    # Upload the data as a CSV file and send the request to the API
    with tempfile.NamedTemporaryFile(suffix=".csv") as file:
        data.to_csv(file.name, index=False)
        endpoint_url = f"{API_URL}/treelists/{treelist_id}/data"
        response = SESSION.patch(endpoint_url, files={"file": file})

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return Treelist(**response.json())


def delete_treelist(treelist_id: str, dataset_id: str = None) -> list[Treelist]:
    """
    Delete a Treelist by its ID. Returns a list of Treelist objects for the
    passed dataset ID. By default, all Treelists are returned.

    Parameters
    ----------
    treelist_id : str
        The ID of the Treelist to delete.
    dataset_id : str, optional
        The ID of the dataset to filter remaining Treelists for,
        by default None.

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
    if dataset_id:
        endpoint_url += f"?dataset_id={dataset_id}"
    response = SESSION.delete(endpoint_url)

    # Raise an error if the API returns an unsuccessful status code
    if response.status_code != 200:
        raise HTTPError(response.json())

    return [Treelist(**treelist) for treelist in response.json()["treelists"]]


def delete_all_treelists(dataset_id: str = None) -> list[Treelist]:
    """
    Delete all Treelists. By default, all Treelists are deleted. Optionally,
    pass a dataset ID to delete all Treelists for a specific dataset. Returns a
    list of remaining Treelist objects.

    This is a recursive delete that will remove all Fuelgrids associated with
    each Treelist.

    Parameters
    ----------
    dataset_id : str, optional
        The ID of the Dataset to delete Treelists for, by default None.

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
