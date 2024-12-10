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
