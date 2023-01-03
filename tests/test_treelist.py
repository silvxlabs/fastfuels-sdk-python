"""
Test treelist object and endpoints.
"""

# Internal imports
from fastfuels_sdk.datasets import *
from fastfuels_sdk.treelists import *

# Core imports
from time import sleep
from uuid import uuid4
from datetime import datetime

# External imports
import pytest
import pandas as pd
from requests.exceptions import HTTPError

# Create a test dataset
DATASET = create_dataset(name="test_dataset", description="test dataset",
                         spatial_data="3b8e4cf24c8047de8e13aed745fd5bdb")

TREELIST_STATUS_LIST = ["Queued", "Generating", "Computing Metrics",
                        "Uploading", "Finished"]


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
    Test the get Treelist Data endpoint.
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

    # # Check that the treelist data has the correct columns
    # assert set(treelist_data.columns) == set(["id", "x", "y", "fuelgrid_id"])

    # # Check that the treelist data has the correct number of rows
    # num_df_trees = len(treelist_data)
    # num_api_trees = int(new_treelist.summary["area"] * new_treelist.summary["trees_per_area"])
    # assert num_df_trees == num_api_trees
    #
    # # Compute basal area per hectare and compare to the summary
    # df_ba = (np.pi * np.square(treelist_data["DIA_cm"] / 2) / 10000).sum()
    # df_ba_per_ha = df_ba / new_treelist.summary["area"]
    # api_ba_per_ha = new_treelist.summary["basal_area_per_area"]
    # assert df_ba_per_ha == pytest.approx(api_ba_per_ha, rel=0.01)


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
    while treelist.status != "Finished":
        treelist = get_treelist(treelist.id)
        sleep(1)

    # Load the test treelist data csv as a dataframe
    upload_data = pd.read_csv("tests/test-data/test_update_treelist_data.csv")

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
    upload_data = pd.read_csv("tests/test-data/test_update_treelist_data.csv")

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
        "tests/test-data/test_update_bad_treelist_data.csv")

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


def test_delete_all_treelists():
    """
    Test the delete all Treelists endpoint.
    """
    # Create a new treelist
    new_treelist = test_create_treelist()

    # Let the treelist finish generating before deleting
    while new_treelist.status != "Finished":
        new_treelist = get_treelist(new_treelist.id)
        sleep(1)

    # Delete all treelists
    delete_all_treelists()

    # Check that the treelist was deleted. Get request should return 404.
    with pytest.raises(HTTPError):
        get_treelist(new_treelist.id)

    # Check that the treelist was deleted from the dataset treelist list
    dataset = get_dataset(DATASET.id)
    assert new_treelist.id not in [treelist_id for treelist_id in
                                   dataset.treelists]

    # Check that the dataset no longer has any treelists
    assert len(dataset.treelists) == 0
