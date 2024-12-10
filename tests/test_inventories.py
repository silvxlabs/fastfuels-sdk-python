"""
tests/test_inventories.py
"""

# Internal imports
from tests.utils import create_default_domain
from fastfuels_sdk.inventories import Inventories, TreeInventory
from fastfuels_sdk.client_library.exceptions import NotFoundException

# External imports
import pytest


@pytest.fixture(scope="module")
def test_domain():
    """Fixture that creates a test domain to be used by the tests"""
    domain = create_default_domain()

    # Return the domain for use in tests
    yield domain

    # Cleanup: Delete the domain after the tests
    domain.delete()


@pytest.fixture(scope="module")
def test_inventories(test_domain):
    """Fixture that creates a test inventories object to be used by the tests"""
    inventories = Inventories.from_domain(test_domain)

    # Return the inventory for use in tests
    yield inventories

    # Cleanup: Handled by the test_domain fixture


class TestInventoriesFromId:
    def test_success(self, test_domain):
        """
        Tests whether inventories are successfully created and initialized from the given domain.

        The function verifies the successful creation of an `Inventories` object based on the
        provided domain identifier. It asserts that the resulting object is not `None`, its type
        matches the expected `Inventories` class, and it correctly initializes with the domain's
        ID and a `None` tree attribute.
        """
        inventories = Inventories.from_domain_id(test_domain)
        assert inventories is not None
        assert isinstance(inventories, Inventories)
        assert inventories.domain_id == test_domain.id
        assert inventories.tree is None

    def test_bad_domain_id(self, test_domain):
        """
        This function tests handling of a domain object with an invalid ID. It creates a copy of the provided
        test domain with its `id` attribute modified to an invalid value. When attempting to retrieve
        inventories based on this modified test domain, it expects a `NotFoundException` to be raised.
        """
        bad_test_domain = test_domain.model_copy(deep=True)
        bad_test_domain.id = "bad_id"
        with pytest.raises(NotFoundException):
            Inventories.from_domain(bad_test_domain)


class TestGetInventories:
    def test_default(self, test_inventories):
        """
        Tests whether inventories are successfully fetched and updated using assignment.
        """
        new_inventories = test_inventories.get()
        assert new_inventories is not None
        assert isinstance(new_inventories, Inventories)
        assert new_inventories is not test_inventories
        assert new_inventories.domain_id == test_inventories.domain_id
        assert new_inventories.tree == test_inventories.tree

    def test_in_place(self, test_inventories):
        """
        Tests whether inventories are successfully fetched and updated in place.
        """
        test_inventories.get(in_place=True)
        assert test_inventories is not None
        assert isinstance(test_inventories, Inventories)

    def test_in_place_with_assignment(self, test_inventories):
        """
        Tests whether inventories are successfully fetched and updated in place with assignment.
        """
        new_inventories = test_inventories.get(in_place=True)
        assert new_inventories is test_inventories
        assert new_inventories.domain_id == test_inventories.domain_id
        assert new_inventories.tree == test_inventories.tree
