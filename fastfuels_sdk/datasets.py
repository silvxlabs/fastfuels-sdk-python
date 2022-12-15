"""
Dataset class and endpoints for the FastFuels SDK.
"""

# Internal imports
from . import SESSION, API_URL
from fastfuels_sdk.treelists import Treelist, create_treelist, list_treelists

# Core imports
import json
from datetime import datetime

# External imports
from requests.exceptions import HTTPError


class Dataset:
    """
    Dataset class for the FastFuels SDK.

    Attributes
    ----------
    id : str
        The unique identifier for the dataset.
    name : str
        The name of the dataset.
    description : str
        A description of the dataset.
    created_on : datetime
        The date and time the dataset was created.
    spatial_data : dict
        The spatial data for the dataset.
    tags : list[str]
        A list of tags for the dataset.
    fvs_variant : str
        The FVS variant used to generate the dataset.
    version : str
        The version of FastFuels used to create the dataset.
    treelists : list[str]
        A list of treelist IDs associated with the dataset.
    fuelgrids : list[str]
        A list of fuelgrid IDs associated with the dataset.

    Methods
    -------
    get_dataset(dataset_id: str)
        Get a dataset by its ID.

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
            The version of FastFuels used to create the dataset.
        treelists : list[str]
            A list of treelist IDs associated with the dataset.
        fuelgrids : list[str]
            A list of fuelgrid IDs associated with the dataset.
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

    def get(self):
        """
        Returns an up-to-date snapshot of the dataset resource.

        Returns
        -------
        Dataset
            Dataset object.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        return get_dataset(self.id)

    def update(self, name: str = None, description: str = None,
               tags: list = None, inplace: bool = False):
        """
        Update a dataset resource. The attributes that can be updated are name,
        description, and tags.

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
        Create a treelist from the dataset.

        Returns
        -------
        Treelist
            Treelist object.

        """
        return create_treelist(self.id, name, description, method)

    def list_treelists(self) -> list[Treelist]:
        """
        Get a list of treelist IDs associated with the dataset.

        Returns
        -------
        list[Treelist]
            List of Treelist objects.

        Raises
        ------
        HTTPError
            If the API returns an error.
        """
        return list_treelists(self.id)

    # TODO: Add a method to list fuelgrids associated with a dataset
    def list_fuelgrids(self):
        pass

    def delete(self):
        """
        Deletes the current dataset resource. This is a recursive delete
        operation so any TreeLists and FuelGrids associated with the dataset
        will also be deleted.

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
    spatial data in the FastFuels API. A Dataset can be created from a feature
    id created through the GIS API or from a geoJSON. Datasets can be used to
    create TreeLists for distributing trees on a landscape, and FuelGrids to
    voxelize a TreeList for use in a 3D model.

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

    return Dataset(**response.json())


def get_dataset(dataset_id: str) -> Dataset:
    """
    Get a dataset object by its ID.

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
    Get a list of all datasets.

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
    Update a dataset resource. The attributes that can be updated are name,
    description, and tags.

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
    Delete a dataset resource.

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
    Delete all dataset resources.

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
