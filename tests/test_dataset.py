"""
Test dataset endpoints and objects.
"""

# Internal imports
from fastfuels_sdk.datasets import *

# Core imports
import json
from uuid import uuid4
from datetime import datetime

# External imports
import pytest
from requests.exceptions import HTTPError


class TestDatasetObject:
    dataset = create_dataset(
        name="test",
        description="test dataset with sdk",
        spatial_data="3b8e4cf24c8047de8e13aed745fd5bdb"
    )

    def test_get_method(self):
        """
        Test the get method of the Dataset object.
        """
        new_dataset = self.dataset.get()

        # Check that the dataset object is the same as the one returned by the
        # get method
        assert new_dataset.id == self.dataset.id
        assert new_dataset.name == self.dataset.name
        assert new_dataset.description == self.dataset.description
        assert new_dataset.spatial_data == self.dataset.spatial_data
        assert new_dataset.tags == self.dataset.tags
        assert new_dataset.created_on == self.dataset.created_on
        assert new_dataset.fvs_variant == self.dataset.fvs_variant
        assert new_dataset.treelists == self.dataset.treelists
        assert new_dataset.fuelgrids == self.dataset.fuelgrids
        assert new_dataset.version == self.dataset.version

    def test_update_method(self):
        """
        Test the update method of the Dataset object.
        """
        new_dataset = self.dataset.update(
            name="new name",
            description="new description",
            tags=["new-tag"])

        # Check that the dataset object is the same as the one returned by the
        # update method
        assert new_dataset.id == self.dataset.id
        assert new_dataset.name == "new name"
        assert new_dataset.description == "new description"
        assert new_dataset.spatial_data == self.dataset.spatial_data
        assert new_dataset.tags == ["new-tag"]
        assert new_dataset.created_on == self.dataset.created_on
        assert new_dataset.fvs_variant == self.dataset.fvs_variant
        assert new_dataset.treelists == self.dataset.treelists
        assert new_dataset.fuelgrids == self.dataset.fuelgrids
        assert new_dataset.version == self.dataset.version

    def test_update_method_inplace(self):
        """
        Test the update method of the Dataset object using the inplace argument.
        """
        self.dataset.update(
            name="new name",
            description="new description",
            tags=["new-tag"],
            inplace=True)

        # Check that the dataset object is the same as the one returned by the
        # update method
        assert self.dataset.name == "new name"
        assert self.dataset.description == "new description"
        assert self.dataset.tags == ["new-tag"]

    def test_delete_method(self):
        """
        Test the delete method of the Dataset object.
        """
        old_id = self.dataset.id
        self.dataset.delete()
        with pytest.raises(HTTPError):
            get_dataset(old_id)


def test_create_dataset_feature():
    """
    Test creating a dataset.
    """
    # Create a dataset
    dataset = create_dataset(
        name="test",
        description="test dataset with sdk",
        spatial_data="3b8e4cf24c8047de8e13aed745fd5bdb"
    )

    # Check the dataset attributes
    assert dataset.id is not None
    assert dataset.name == "test"
    assert dataset.description == "test dataset with sdk"
    assert isinstance(dataset.created_on, datetime)
    assert isinstance(dataset.spatial_data, dict)
    assert dataset.spatial_data["epsg"] == 4326
    assert dataset.spatial_data["bbox"] == {
        "west": -113.94717919590558,
        "east": -113.94615426856866,
        "south": 46.82586367573463,
        "north": 46.826770523885266
    }
    assert dataset.tags == []
    assert dataset.fvs_variant == "IE"
    assert dataset.version is not None
    assert dataset.treelists == []
    assert dataset.fuelgrids == []

    return dataset


def test_create_dataset_geojson():
    """
    Test creating a dataset.
    """
    # Load the geojson
    with open("tests/test-data/test.geojson", "r") as f:
        geojson = json.load(f)

    # Create a dataset
    dataset = create_dataset(
        name="test",
        description="test dataset with sdk",
        spatial_data=geojson
    )

    # Check the dataset attributes
    assert dataset.id is not None
    assert dataset.name == "test"
    assert dataset.description == "test dataset with sdk"
    assert isinstance(dataset.created_on, datetime)
    assert isinstance(dataset.spatial_data, dict)
    assert dataset.spatial_data["epsg"] == 4326
    assert dataset.spatial_data["bbox"] == {
        "west": -122.56096774114704,
        "east": -122.54357448500281,
        "south": 40.894586153305994,
        "north": 40.90793941697117
    }
    assert dataset.tags == []
    assert dataset.fvs_variant == "CA"
    assert dataset.version is not None
    assert dataset.treelists == []
    assert dataset.fuelgrids == []


def test_create_dataset_bad_feature_id():
    """
    Test creating a dataset with a bad feature id.
    """
    # Create a dataset
    with pytest.raises(HTTPError):
        create_dataset(
            name="test",
            description="test dataset with sdk",
            spatial_data=uuid4().hex
        )


def test_create_dataset_bad_geojson():
    """
    Test creating a dataset with a bad geojson.
    """
    # Create a dataset
    with pytest.raises(HTTPError):
        create_dataset(
            name="test",
            description="test dataset with sdk",
            spatial_data={"": uuid4().hex}
        )


def test_get_dataset_function():
    """
    Test getting a dataset by its ID.
    """
    # Create a dataset
    original_dataset = test_create_dataset_feature()

    # Get the dataset by its ID
    new_dataset = get_dataset(original_dataset.id)

    # Check the dataset attributes
    assert new_dataset.id is not None
    assert new_dataset.name == "test"
    assert new_dataset.description == "test dataset with sdk"
    assert isinstance(new_dataset.created_on, datetime)
    assert isinstance(new_dataset.spatial_data, dict)
    assert new_dataset.spatial_data["epsg"] == 4326
    assert new_dataset.spatial_data["bbox"] == {
        "west": -113.94717919590558,
        "east": -113.94615426856866,
        "south": 46.82586367573463,
        "north": 46.826770523885266
    }
    assert new_dataset.tags == []
    assert new_dataset.fvs_variant == "IE"
    assert new_dataset.version is not None
    assert new_dataset.treelists == []
    assert new_dataset.fuelgrids == []

    # Check that the two datasets are the same
    assert original_dataset.id == new_dataset.id
    assert original_dataset.name == new_dataset.name
    assert original_dataset.description == new_dataset.description
    assert original_dataset.created_on == new_dataset.created_on
    assert original_dataset.spatial_data == new_dataset.spatial_data
    assert original_dataset.tags == new_dataset.tags
    assert original_dataset.fvs_variant == new_dataset.fvs_variant
    assert original_dataset.version == new_dataset.version
    assert original_dataset.treelists == new_dataset.treelists
    assert original_dataset.fuelgrids == new_dataset.fuelgrids


def test_get_dataset_bad_id():
    """
    Test getting a dataset with a bad ID.
    """
    # Get the dataset by its ID
    with pytest.raises(HTTPError):
        get_dataset(uuid4().hex)


def test_list_datasets():
    """
    Test getting a list of 
    """
    # Create a dataset
    dataset = test_create_dataset_feature()

    # Get the list of datasets
    dataset_list = list_datasets()

    # Check the dataset list
    assert len(dataset_list) > 0
    assert isinstance(dataset_list[0], Dataset)
    assert dataset.id in [d.id for d in dataset_list]


def test_update_dataset():
    """
    Test updating a dataset.
    """
    # Create a dataset
    old_dataset = test_create_dataset_feature()

    # Update the dataset
    new_dataset = update_dataset(
        dataset_id=old_dataset.id,
        name="new name",
        description="new description",
        tags=["new-tag"])

    # Check the dataset attributes
    assert new_dataset.id is not None
    assert new_dataset.name == "new name"
    assert new_dataset.description == "new description"
    assert isinstance(new_dataset.created_on, datetime)
    assert isinstance(new_dataset.spatial_data, dict)
    assert new_dataset.spatial_data["epsg"] == 4326
    assert new_dataset.spatial_data["bbox"] == {
        "west": -113.94717919590558,
        "east": -113.94615426856866,
        "south": 46.82586367573463,
        "north": 46.826770523885266
    }
    assert new_dataset.tags == ["new-tag"]
    assert new_dataset.fvs_variant == "IE"
    assert new_dataset.version is not None
    assert new_dataset.treelists == []
    assert new_dataset.fuelgrids == []


def test_update_dataset_bad_id():
    """
    Test updating a dataset with a bad ID.
    """
    # Update the dataset
    with pytest.raises(HTTPError):
        update_dataset(
            dataset_id=uuid4().hex,
            name="new name",
            description="new description",
            tags=["new-tag"])


def test_delete_dataset():
    """
    Test deleting a dataset.
    """
    # Create a dataset
    dataset_to_delete = test_create_dataset_feature()

    # Create another dataset to make sure the list is not empty
    dataset_to_stay = test_create_dataset_feature()

    # Delete the dataset
    dataset_list = delete_dataset(dataset_to_delete.id)

    # Check that the dataset was deleted
    assert len(dataset_list) > 0
    assert isinstance(dataset_list[0], Dataset)
    assert dataset_to_stay.id in [d.id for d in dataset_list]
    assert dataset_to_delete not in dataset_list

    # Try to get the dataset
    with pytest.raises(HTTPError):
        get_dataset(dataset_to_delete.id)


def test_delete_dataset_bad_id():
    """
    Test deleting a dataset with a bad ID.
    """
    # Delete the dataset
    with pytest.raises(HTTPError):
        delete_dataset(uuid4().hex)


def test_delete_all_datasets():
    """
    Test deleting all 
    """
    # Create a dataset
    dataset_to_delete = test_create_dataset_feature()

    # Delete all datasets
    delete_all_datasets()

    # Check if there are any datasets
    dataset_list = list_datasets()

    # Check that the dataset was deleted
    assert len(dataset_list) == 0

    # Try to get the dataset
    with pytest.raises(HTTPError):
        get_dataset(dataset_to_delete.id)
