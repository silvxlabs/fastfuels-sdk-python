"""
Test treelist object and endpoints.
"""

# Internal imports
from fastfuels_sdk.datasets import *
from fastfuels_sdk.treelists import *

# Core imports
import json
from uuid import uuid4
from datetime import datetime

# External imports
import pytest
import pandas as pd
from requests.exceptions import HTTPError

# Create a test dataset
DATASET = create_dataset(name="test_dataset", description="test dataset",
                         spatial_data="3b8e4cf24c8047de8e13aed745fd5bdb")

TREELIST_STATUS_LIST = ["Queued", "Generating", "Uploading", "Finished"]


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


def test_update_treelist():
    """
    Test the update Treelist endpoint.
    """
    # Create a new treelist
    new_treelist = test_create_treelist()

    # Let the treelist finish generating before updating
    while new_treelist.status != "Finished":
        new_treelist = get_treelist(new_treelist.id)

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


def test_delete_treelist():
    """
    Test the delete Treelist endpoint.
    """
    # Create a new treelist
    new_treelist = test_create_treelist()

    # Let the treelist finish generating before deleting
    while new_treelist.status != "Finished":
        new_treelist = get_treelist(new_treelist.id)

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
