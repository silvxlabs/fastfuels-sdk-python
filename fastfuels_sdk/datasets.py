"""
Dataset class and endpoints for the FastFuels SDK.
"""
# Core imports
from __future__ import annotations
import json
from datetime import datetime

# Internal imports
from fastfuels_sdk.api import SESSION, API_URL
from fastfuels_sdk._base import FastFuelsResource
from fastfuels_sdk.treelists import (Treelist, create_treelist, list_treelists,
                                     delete_all_treelists)
from fastfuels_sdk.fuelgrids import (Fuelgrid, list_fuelgrids,
                                     delete_all_fuelgrids)

# External imports
from requests.exceptions import HTTPError


class Dataset(FastFuelsResource):
    """
    Class representing the Dataset resource in the FastFuels API. It represents
    a collection of spatial data, TreeList, and Fuelgrid resources, alongside
    associated metadata. The spatial data stored in the Dataset resource is used
    to generate Treelists and Fuelgrids.
    """

    def __init__(self, id: str, name: str, description: str,
                 created_on: str, spatial_data: dict, tags: list[str],
                 fvs_variant: str, version: str, treelists: list[str],
                 fuelgrids: list[str]):
        """
        Initialize a Dataset object.

        Parameters
        ----------
        id : str
            The unique identifier for the dataset.
        name : str
            The name of the dataset.
        description : str
            A description of the dataset.
        created_on : str
            The date and time the dataset was created.
        spatial_data : dict
            The spatial data for the dataset.
        tags : list[str]
            A list of tags for the dataset.
        fvs_variant : str
            The FVS variant used to generate the dataset.
        version : str
            The version of FastFuels used to create the dataset. The data is
            read in ISO 8601 format and converted to a datetime object.
        treelists : list[str]
            A list of treelist IDs associated with the dataset.
        fuelgrids : list[str]
            A list of Fuelgrid IDs associated with the dataset.
        """
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.created_on: datetime = datetime.fromisoformat(created_on)
        self.spatial_data: dict = spatial_data
        self.tags: list[str] = tags if tags else []
        self.fvs_variant: str = fvs_variant
        self.version: str = version
        self.treelists: list[str] = treelists
        self.fuelgrids: list[str] = fuelgrids

    def refresh(self, inplace: bool = False):
        """
        Returns an up-to-date snapshot of the dataset resource. This method
        corresponds to the GET /datasets/{id} endpoint for an existing
        Dataset resource.

        If inplace is True, the current Dataset object will be updated with the
        new values. Otherwise, a new Dataset object will be returned.

        Returns
        -------
        Dataset or None
            Dataset object if inplace is True, otherwise None.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        refreshed_dataset = get_dataset(self.id)
        if inplace:
            self.__dict__.update(refreshed_dataset.__dict__)
        else:
            return refreshed_dataset

    def update(self, name: str = None, description: str = None,
               tags: list = None, inplace: bool = False):
        """
        Update a Dataset resource. The attributes that can be updated are
        name, description, and tags. The spatial data cannot be updated for
        an existing Dataset.

        If inplace is True, the current Dataset object will be updated with the
        new values. Otherwise, a new Dataset object will be returned.

        Parameters
        ----------
        name : str, optional
            Name of the dataset to update, by default None.
        description : str, optional
            Description of the dataset to update, by default None.
        tags : list, optional
            Tags for the dataset to update, by default None.
        inplace : bool, optional
            Whether to update the dataset object in place, or return a new
            dataset object. By default False.

        Returns
        -------
        Dataset
            Updated Dataset object.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        updated_dataset = update_dataset(self.id, name, description, tags)
        if inplace:
            self.__dict__.update(updated_dataset.__dict__)
        else:
            return updated_dataset

    def create_treelist(self, name: str, description: str = "",
                        method: str = "random") -> Treelist:
        """
        Create a new Treelist resource associated with the current Dataset.

        This method creates a new Treelist from the spatial bounding box of
        the current Dataset. A Treelist resource contains metadata about the
        Treelist and associated Fuelgrid resources. Once a Treelist resource
        is created and enters the "Finished" status, the data can be accessed
        as a Pandas DataFrame through the get_treelist_data() method.

        Parameters
        ----------
        name : str
            The name to assign to the new Treelist.
        description : str, optional
            A description of the new Treelist. Defaults to an empty string.
        method : str, optional
            The method to use for generating the Treelist. Currently, only
            "random" is supported. Defaults to "random".

        Returns
        -------
        Treelist
            The new Treelist object.

        Raises
        ------
        HTTPError
            If the API returns an error when creating the Treelist.
        """
        return create_treelist(self.id, name, description, method)

    def list_treelists(self) -> list[Treelist]:
        """
        Retrieve a list of all Treelist resources associated with the current
        Dataset.

        This method fetches all Treelists that are associated with the
        current Dataset from the FastFuels API and returns them as a list of
        Treelist objects.

        Returns
        -------
        list[Treelist]
            A list of Treelist objects associated with the current Dataset. If
            no Treelists are associated with the Dataset, returns an empty list.

        Raises
        ------
        HTTPError
            If the FastFuels API returns an error when attempting to retrieve
            the list of Treelist resources.
        """
        return list_treelists(dataset_id=self.id)

    def list_fuelgrids(self) -> list[Fuelgrid]:
        """
        Retrieve a list of all Fuelgrid resources associated with the current
        Dataset.

        This method fetches all Fuelgrids that are associated with the
        current Dataset from the FastFuels API and returns them as a list of
        Fuelgrid objects.

        Returns
        -------
        list[Fuelgrid]
            A list of Fuelgrid objects associated with the current Dataset. If
            no Fuelgrids are associated with the Dataset, returns an empty list.

        Raises
        ------
        HTTPError
            If the FastFuels API returns an error when attempting to retrieve
            the list of Fuelgrid resources.
        """
        return list_fuelgrids(dataset_id=self.id)

    def delete_treelists(self):
        """
        Delete all Treelist resources associated with the current Dataset.

        This method sends a request to the FastFuels API to delete all
        Treelist resources that are associated with the current Dataset. This
        is a recursive delete operation and will also remove all Fuelgrids
        associated with each Treelist.

        Please note that the operation is irreversible and all data associated
        with the Treelists and Fuelgrids will be lost.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If the FastFuels API returns an error when attempting to delete the
            Treelist resources.
        """
        delete_all_treelists(dataset_id=self.id)

    def delete_fuelgrids(self):
        """
        Deletes all Fuelgrid resources associated with the current Dataset.

        This method sends a request to the FastFuels API to delete all
        Fuelgrid resources that are associated with the current Dataset.
        Please note that this operation is irreversible and all data
        associated with the Fuelgrids will be permanently deleted.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If the FastFuels API returns an error when attempting to delete the
            Fuelgrid resources.
        """
        delete_all_fuelgrids(dataset_id=self.id)

    def delete(self) -> None:
        """
        Deletes the current Dataset instance along with all its associated
        Treelists and Fuelgrids.

        This method performs a recursive deletion operation, meaning that it
        not only deletes the Dataset object itself, but also all associated
        Treelist and Fuelgrid objects linked to this Dataset. This operation
        is irreversible and leads to the permanent removal of all related
        data from the FastFuels API.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If the FastFuels API returns an error when attempting to delete the
            Dataset resource and its associated Treelists and Fuelgrids.
        """
        delete_dataset(self.id)


def create_dataset(name: str, description: str, spatial_data: dict,
                   tags: list = None) -> Dataset:
    """
    Creates a new FastFuels Dataset. A Dataset is the primary object for storing
    spatial data in the FastFuels API. The primary role of a Dataset is to
    store spatial data and to provide a container for Treelists and Fuelgrids.
    All data products generated by FastFuels are associated with a Dataset.

    Dataset spatial data can be provided as a GeoJSON dictionary. The spatial
    data must be a valid GeoJSON FeatureCollection object.

    Parameters
    ----------
    name : str
        Name of the dataset.
    description : str
        Description of the dataset.
    spatial_data : dict
        Spatial data for the dataset as a GeoJSON FeatureCollection object.
    tags : list, optional
        Tags for the dataset, by default None.

    Returns
    -------
    Dataset
        Dataset object.

    Raises
    ------
    HTTPError
        If the API returns an error.
    """
    # Put together the request payload for the API call
    payload_dict = {
        "name": name,
        "description": description,
        "tags": tags
    }
    key = "feature_id" if isinstance(spatial_data, str) else "data"
    payload_dict["spatial_data"] = {key: spatial_data}
    payload = json.dumps(payload_dict)

    # Send the request to the API
    endpoint_url = f"{API_URL}/datasets"
    response = SESSION.post(endpoint_url, data=payload)

    # Raise an error if the API returns an error
    if response.status_code != 201:
        raise HTTPError(response.json())

    return Dataset(**response.json())


def get_dataset(dataset_id: str) -> Dataset:
    """
    Returns a Dataset object populated with the resource data for a given
    Dataset ID.

    Parameters
    ----------
    dataset_id : str
        The unique identifier for the dataset.

    Returns
    -------
    Dataset
        Dataset object.

    Raises
    ------
    HTTPError
        If the API returns an error.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/datasets/{dataset_id}"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an error
    if response.status_code != 200:
        raise HTTPError(response.json())

    return Dataset(**response.json())


def list_datasets() -> list[Dataset]:
    """
    Get a list of all Dataset objects for the current user.

    Returns
    -------
    list[Dataset]
        List of Dataset objects.

    Raises
    ------
    HTTPError
        If the API returns an error.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/datasets"
    response = SESSION.get(endpoint_url)

    # Raise an error if the API returns an error
    if response.status_code != 200:
        raise HTTPError(response.json())

    return [Dataset(**dataset) for dataset in response.json()["datasets"]]


def update_dataset(dataset_id: str, name: str = None, description: str = None,
                   tags: list = None) -> Dataset:
    """
    Update a Dataset resource. The attributes that can be updated are name,
    description, and tags. The spatial data cannot be updated for an existing
    Dataset.

    Parameters
    ----------
    dataset_id : str
        The unique identifier for the dataset.
    name : str, optional
        Name of the dataset to update, by default None.
    description : str, optional
        Description of the dataset to update, by default None.
    tags : list, optional
        Tags for the dataset to update, by default None.

    Returns
    -------
    Dataset
        Updated Dataset object.

    Raises
    ------
    HTTPError
        If the API returns an error.
    ValueError
        If no attributes are provided to update.
    """
    # At least one of the optional parameters must be provided
    if name is None and description is None and tags is None:
        raise ValueError("At least one of the optional parameters must be "
                         "provided.")

    # Put together the request payload for the API call
    payload_dict = {}
    if name:
        payload_dict["name"] = name
    if description:
        payload_dict["description"] = description
    if tags:
        payload_dict["tags"] = tags
    payload = json.dumps(payload_dict)

    # Send the request to the API
    endpoint_url = f"{API_URL}/datasets/{dataset_id}"
    response = SESSION.patch(endpoint_url, data=payload)

    if response.status_code != 200:
        raise HTTPError(response.json())

    return Dataset(**response.json())


def delete_dataset(dataset_id: str) -> list[Dataset]:
    """
    Delete a Dataset resource. This is a recursive delete, meaning that all
    Treelists and Fuelgrids associated with the dataset will also be deleted.
    Returns a list of the remaining Dataset objects for the current user.

    Parameters
    ----------
    dataset_id : str
        The unique identifier for the dataset.

    Raises
    ------
    HTTPError
        If the API returns an error.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/datasets/{dataset_id}"
    response = SESSION.delete(endpoint_url)

    # Raise an error if the API returns an error
    if response.status_code != 200:
        raise HTTPError(response.json())

    return [Dataset(**dataset) for dataset in response.json()["datasets"]]


def delete_all_datasets() -> None:
    """
    Delete all Dataset resources. This is a recursive delete, meaning that all
    Treelists and Fuelgrids associated with the user's Datasets will also be
    deleted.

    Raises
    ------
    HTTPError
        If the API returns an error.
    """
    # Send the request to the API
    endpoint_url = f"{API_URL}/datasets"
    response = SESSION.delete(endpoint_url)

    # Raise an error if the API returns an error
    if response.status_code != 200:
        raise HTTPError(response.json())

    return None
