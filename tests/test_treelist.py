"""
Test treelist object and endpoints.
"""

# Internal imports
import sys

sys.path.append("../")
from fastfuels_sdk.datasets import *
from fastfuels_sdk.treelists import *

# Core imports
import json
from time import sleep
from uuid import uuid4
from datetime import datetime

# External imports
import pytest
import pandas as pd
from requests.exceptions import HTTPError


def setup_module(module):
    with open("test-data/blue_mtn_100m.geojson") as f:
        spatial_data = json.load(f)

    # Create a test dataset
    global DATASET
    DATASET = create_dataset(name="test_dataset", description="test dataset",
                             spatial_data=spatial_data)


TREELIST_STATUS_LIST = ["Queued", "Processing", "Computing Metrics",
                        "Uploading", "Finished"]


# class TestTreelistObject:
#     """
#     Test the Treelist object.
#     """
#     dataset = create_dataset(
#         name="test",
#         description="test dataset with sdk",
#         spatial_data="3b8e4cf24c8047de8e13aed745fd5bdb"
#     )
#     treelist = dataset.create_treelist(
#         name="test",
#         description="test treelist with sdk",
#     )
#
#     def test_get_data(self):
#         """
#         Test the get data method.
#         """
#         # Wait for the treelist to finish generating
#         while self.treelist.status != "Finished":
#             self.treelist = get_treelist(self.treelist.id)
#             sleep(1)
#
#         # Get the treelist data
#         treelist_data = self.treelist.get_data()
#         assert isinstance(treelist_data, pd.DataFrame)
#         assert len(treelist_data) != 0
#         assert list(treelist_data.columns) == ['SPCD', 'DIA_cm', 'HT_m',
#                                                'STATUSCD', 'CBH_m',
#                                                'CROWN_RADIUS_m', 'X_m', 'Y_m']
#
#     def test_update(self):
#         """
#         Test the update method.
#         """
#         updated_treelist = self.treelist.update(name="new_name",
#                                                 description="new_description")
#         assert updated_treelist.name == "new_name"
#         assert updated_treelist.description == "new_description"
#
#     def test_update_data(self):
#         """
#         Test the update data method.
#         """
#         # Load the test treelist data csv as a dataframe
#         upload_data = pd.read_csv(
#             "test-data/test_update_treelist_data.csv")
#
#         # Update the treelist data
#         updated_treelist = self.treelist.update_data(upload_data)
#         updated_df = updated_treelist.get_data()
#
#         # Check that the treelist data was updated
#         assert len(updated_df) == len(upload_data)
#
#     def test_delete(self):
#         """
#         Test the delete method.
#         """
#         # Delete the treelist
#         self.treelist.delete()
#
#         # Check that the treelist was deleted. Get request should return 404.
#         with pytest.raises(HTTPError):
#             get_treelist(self.treelist.id)
#
#         # Check that the treelist was deleted from the dataset treelist list
#         dataset = get_dataset(self.dataset.id)
#         assert self.treelist.id not in [treelist_id for treelist_id in
#                                         dataset.treelists]


def test_create_treelist():
    """
    Test creating a treelist.
    """
    treelist = create_treelist(dataset_id=DATASET.id,
                               name="test_treelist",
                               description="test treelist")

    assert treelist.id is not None
    assert treelist.name == "test_treelist"
    assert treelist.description == "test treelist"
    assert treelist.method == "random"
    assert treelist.dataset_id == DATASET.id
    assert treelist.status in TREELIST_STATUS_LIST
    assert isinstance(treelist.summary, dict)
    assert isinstance(treelist.created_on, datetime)
    assert treelist.fuelgrids == []
    assert isinstance(treelist.version, str)

    dataset = get_dataset(DATASET.id)
    assert treelist.id in [treelist_id for treelist_id in dataset.treelists]

    return treelist


def test_create_treelist_bad_dataset_id():
    """
    Test creating a treelist with a bad dataset id.
    """
    with pytest.raises(HTTPError):
        create_treelist(dataset_id=uuid4().hex, name="test_treelist",
                        description="test treelist")


def test_get_treelist():
    """
    Test the get Treelist endpoint.
    """
    new_treelist = test_create_treelist()
    treelist = get_treelist(new_treelist.id)

    assert treelist.id == new_treelist.id
    assert treelist.name == new_treelist.name
    assert treelist.description == new_treelist.description
    assert treelist.method == new_treelist.method
    assert treelist.dataset_id == new_treelist.dataset_id
    assert treelist.status in TREELIST_STATUS_LIST
    assert isinstance(treelist.summary, dict)
    assert treelist.created_on == new_treelist.created_on
    assert treelist.fuelgrids == new_treelist.fuelgrids
    assert treelist.version == new_treelist.version

    # If the treelist does not have a status of "Complete", repeat
    while treelist.status != "Finished":
        treelist = get_treelist(treelist.id)
        sleep(1)
    assert treelist.status == "Finished"


def test_get_treelist_bad_treelist_id():
    """
    Test the get Treelist endpoint with a bad treelist id.
    """
    with pytest.raises(HTTPError):
        get_treelist(uuid4().hex)


def test_list_treelists():
    """
    Test the list Treelists endpoint.
    """
    new_treelist = test_create_treelist()
    treelists = list_treelists()

    assert isinstance(treelists, list)
    assert len(treelists) > 0
    assert isinstance(treelists[0], Treelist)
    assert new_treelist.id in [treelist.id for treelist in treelists]


def test_get_treelist_data():
    """
    Test the get Treelist data endpoint.
    """
    # Create a new treelist
    new_treelist = test_create_treelist()

    # Let the treelist finish generating before downloading
    while new_treelist.status != "Finished":
        new_treelist = get_treelist(new_treelist.id)
        sleep(1)

    # Download the treelist data
    treelist_data = get_treelist_data(new_treelist.id)

    # Check that the treelist data is a pandas dataframe
    assert isinstance(treelist_data, pd.DataFrame)

    # Check that the treelist data has the correct columns
    assert list(treelist_data.columns) == ['SPCD', 'DIA_cm', 'HT_m', 'STATUSCD',
                                           'CBH_m', 'CROWN_RADIUS_m', 'X_m',
                                           'Y_m']

    # Check that the treelist data has the correct number of live trees
    live_trees = treelist_data[treelist_data["STATUSCD"] == 1]
    num_live_trees = len(live_trees)
    num_api_trees = round(
        new_treelist.summary["area"] * new_treelist.summary["trees_per_area"])
    assert num_live_trees == num_api_trees


def test_get_treelist_data_ca():
    with open("test-data/ca_geojson.geojson") as f:
        spatial_data = json.load(f)
    dataset = create_dataset(
        name="ca-test",
        description="test dataset with sdk",
        spatial_data=spatial_data
    )
    treelist = dataset.create_treelist(
        name="ca-test-treelist",
        description="test treelist with sdk",
    )
    treelist.wait_until_finished()
    treelist_data = treelist.get_data()

    assert isinstance(treelist_data, pd.DataFrame)
    assert len(treelist_data) > 2000000


def test_get_treelist_data_bad_treelist_id():
    """
    Test the get Treelist data endpoint with a bad treelist id.
    """
    with pytest.raises(HTTPError):
        get_treelist_data(uuid4().hex)


def test_update_treelist():
    """
    Test the update Treelist endpoint.
    """
    # Create a new treelist
    new_treelist = test_create_treelist()

    # Let the treelist finish generating before updating
    while new_treelist.status != "Finished":
        new_treelist = get_treelist(new_treelist.id)
        sleep(1)

    # Update the treelist
    update_treelist(new_treelist.id, name="new_name",
                    description="new_description")

    # Check that the treelist was updated
    updated_treelist = get_treelist(new_treelist.id)
    assert updated_treelist.name == "new_name"
    assert updated_treelist.description == "new_description"


def test_update_treelist_bad_treelist_id():
    """
    Test the update Treelist endpoint with a bad treelist id.
    """
    with pytest.raises(HTTPError):
        update_treelist(uuid4().hex, name="new_name",
                        description="new_description")


def test_update_treelist_data():
    """
    Test the update Treelist Data endpoint.
    """
    # Create a new treelist
    treelist = test_create_treelist()

    # Let the treelist finish generating before updating
    treelist.wait_until_finished()

    # Load the test treelist data csv as a dataframe
    upload_data = pd.read_csv("test-data/test_update_treelist_data.csv")

    # Update the treelist data
    updated_treelist = update_treelist_data(treelist.id, upload_data)
    updated_df = get_treelist_data(updated_treelist.id)

    # Check that the treelist data was updated
    assert len(updated_df) == len(upload_data)


def test_update_treelist_data_bad_treelist_id():
    """
    Test the update Treelist Data endpoint with a bad treelist id.
    """
    # Load the test treelist data csv as a dataframe
    upload_data = pd.read_csv("test-data/test_update_treelist_data.csv")

    with pytest.raises(HTTPError):
        update_treelist_data(uuid4().hex, upload_data)


def test_update_treelist_data_bad_data():
    """
    Test the update Treelist Data endpoint with bad data.
    """
    # Create a new treelist
    treelist = test_create_treelist()

    # Let the treelist finish generating before updating
    while treelist.status != "Finished":
        treelist = get_treelist(treelist.id)
        sleep(1)

    # Load the test treelist data csv as a dataframe
    upload_data = pd.read_csv(
        "test-data/test_update_bad_treelist_data.csv")

    with pytest.raises(HTTPError):
        update_treelist_data(treelist.id, upload_data)


def test_delete_treelist():
    """
    Test the delete Treelist endpoint.
    """
    # Create a new treelist
    new_treelist = test_create_treelist()

    # Let the treelist finish generating before deleting
    while new_treelist.status != "Finished":
        new_treelist = get_treelist(new_treelist.id)
        sleep(1)

    # Delete the treelist
    delete_treelist(new_treelist.id)

    # Check that the treelist was deleted. Get request should return 404.
    with pytest.raises(HTTPError):
        get_treelist(new_treelist.id)

    # Check that the treelist was deleted from the dataset treelist list
    dataset = get_dataset(DATASET.id)
    assert new_treelist.id not in [treelist_id for treelist_id in
                                   dataset.treelists]


def test_delete_treelist_bad_treelist_id():
    """
    Test the delete Treelist endpoint with a bad treelist id.
    """
    # Delete the treelist
    with pytest.raises(HTTPError):
        delete_treelist(uuid4().hex)
