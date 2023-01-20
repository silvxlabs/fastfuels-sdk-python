"""
Dataset class and endpoints for the FastFuels SDK.
"""

# Internal imports
from fastfuels_sdk.api import SESSION, API_URL
from fastfuels_sdk.treelists import (Treelist, create_treelist, list_treelists,
                                     delete_all_treelists)
from fastfuels_sdk.fuelgrids import (Fuelgrid, list_fuelgrids,
                                     delete_all_fuelgrids)

# Core imports
import json
from datetime import datetime

# External imports
from requests.exceptions import HTTPError


class Dataset:
    """
    Class representing the Dataset resource. The Dataset resource is the main
    resource in the FastFuels API. It represents a collection of spatial data
    and associated metadata. The spatial data is used to generate Treelists
    and Fuelgrids. CRUD operations are supported both as methods on the
    Dataset object and as standalone functions.

    Attributes
    ----------
    id : str
        The unique identifier for the Dataset.
    name : str
        The name of the Dataset.
    description : str
        A description of the Dataset.
    created_on : datetime
        The date and time the Dataset was created.
    tags : list[str]
        A list of tags for the Dataset.
    spatial_data : dict
        The spatial data for the Dataset.
    fvs_variant : str
        The FVS variant associated with the Dataset's spatial data.
    version : str
        The version of FastFuels used to create the Dataset.
    treelists : list[str]
        A list of treelist IDs associated with the Dataset.
    fuelgrids : list[str]
        A list of fuelgrid IDs associated with the Dataset.

    """

    def __init__(self, dataset_id: str, name: str, description: str,
                 created_on: str, spatial_data: dict, tags: list[str],
                 fvs_variant: str, version: str, treelists: list[str],
                 fuelgrids: list[str]):
        """
        Initialize a Dataset object.

        Parameters
        ----------
        dataset_id : str
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
            A list of fuelgrid IDs associated with the dataset.
        """
        self.id: str = dataset_id
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
        Update a Dataset resource. The attributes that can be updated are name,
        description, and tags. The spatial data cannot be updated for an existing
        Dataset.

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

    def create_treelist(self, name: str, description: str,
                        method: str = "random") -> Treelist:
        """
        # TODO: Add docstring
        Create a treelist from the dataset.

        Returns
        -------
        Treelist
            Treelist object.

        Raises
        ------
        HTTPError
            If the API returns an error.

        """
        return create_treelist(self.id, name, description, method)

    def list_treelists(self) -> list[Treelist]:
        """
        # TODO: Add docstring
        Get a list of Treelist objects associated with the dataset.

        Returns
        -------
        list[Treelist]
            List of Treelist objects.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        return list_treelists(dataset_id=self.id)

    def list_fuelgrids(self) -> list[Fuelgrid]:
        """
        # TODO: Add docstring
        Get a list of Fuelgrid objects associated with the dataset.

        Returns
        -------
        list[Fuelgrid]
            List of Fuelgrid objects.
        """
        return list_fuelgrids(dataset_id=self.id)

    def delete_treelists(self):
        """
        # TODO: Add Docstring
        Delete all treelists associated with the dataset.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        delete_all_treelists(dataset_id=self.id)

    def delete_fuelgrids(self):
        """
        # TODO: Add docstring
        Delete all fuelgrids associated with the dataset.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        delete_all_fuelgrids(dataset_id=self.id)

    def delete(self) -> None:
        """
        Delete a Dataset resource. This is a recursive delete, meaning that all
        Treelists and Fuelgrids associated with the dataset will also be deleted.
        Returns a list of the remaining Dataset objects for the current user.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        delete_dataset(self.id)


def create_dataset(name: str, description: str, spatial_data: str | dict,
                   tags: list = None) -> Dataset:
    """
    Creates a new FastFuels Dataset. A Dataset is the primary object for storing
    spatial data in the FastFuels API. The primary role of a Dataset is to
    store spatial data and to provide a container for Treelists and Fuelgrids.
    All data products generated by FastFuels are associated with a Dataset.

    Dataset spatial data can be provided as a GeoJSON dictionary. The spatial
    data must be a valid GeoJSON FeatureCollection object. Alternatively, the
    spatial data can be provided as a string containing a valid feature ID from
    the Silvx Labs GIS API.

    Parameters
    ----------
    name : str
        Name of the dataset.
    description : str
        Description of the dataset.
    spatial_data : str | dict
        Spatial data for the dataset. Can be a feature id from the GIS API or a
        geoJSON. If the input is a string, it is assumed to be a feature id.
        If the input is a dict, it is assumed to be a geoJSON.
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

    # Rename the "id" key to "dataset_id" for object instantiation
    response_dict = response.json()
    response_dict["dataset_id"] = response_dict.pop("id")

    return Dataset(**response_dict)


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
