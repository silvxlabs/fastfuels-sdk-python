"""
domains.py
"""

# Core imports
import json
from typing import Optional, List

# Internal imports
from fastfuels_sdk.api import get_client
from fastfuels_sdk.client_library.api import DomainsApi
from fastfuels_sdk.client_library.models import (
    Domain as DomainModel,
    CreateDomainRequest,
    ListDomainResponse,
    DomainSortField,
    DomainSortOrder,
    UpdateDomainRequest,
)

_DOMAIN_API = DomainsApi(get_client())


class Domain(DomainModel):
    """ """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_geojson(
        cls,
        geojson: dict,
        name: str = "",
        description: str = "",
        horizontal_resolution: float = 2.0,
        vertical_resolution: float = 1.0,
    ) -> "Domain":
        """ """
        feature_data = {
            **geojson,
            "name": name,
            "description": description,
            "horizontalResolution": horizontal_resolution,
            "verticalResolution": vertical_resolution,
        }

        request = CreateDomainRequest.from_dict(feature_data)
        response = _DOMAIN_API.create_domain(
            create_domain_request=request.model_dump()  # noqa
        )
        return cls(**response.model_dump()) if response else None

    @classmethod
    def from_geodataframe(
        cls,
        geodataframe,
        name: str = "",
        description: str = "",
        horizontal_resolution: float = 2.0,
        vertical_resolution: float = 1.0,
    ):
        """ """
        return cls.from_geojson(
            geojson=json.loads(geodataframe.to_json()),
            name=name,
            description=description,
            horizontal_resolution=horizontal_resolution,
            vertical_resolution=vertical_resolution,
        )

    def get(self, in_place: bool = False) -> "Domain":
        """Retrieve the latest domain data from the API.

        This method fetches the most recent data for this domain from the API. It can
        either update the current Domain instance in-place or return a new instance
        with the fresh data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates the current Domain instance with the new data and returns
            self. If False, returns a new Domain instance with the latest data,
            leaving the current instance unchanged. Default is False.

        Returns
        -------
        Domain
            Either the current Domain instance (if in_place=True) or a new Domain
            instance (if in_place=False) containing the latest data from the API.

        Examples
        --------
        Create new instance with latest data:
        >>> domain = Domain.get_domain("123")
        >>> updated_domain = domain.get()  # domain remains unchanged
        >>> updated_domain is domain
        False

        Update existing instance in-place:
        >>> domain = Domain.get_domain("123")
        >>> domain.get(in_place=True)  # domain is updated
        >>> # Any references to domain now see the updated data

        Notes
        -----
        The default behavior (in_place=False) ensures immutability by returning a new
        instance. This is safer for concurrent operations but requires reassignment if
        you want to retain the updated data. Use in_place=True when you want to
        ensure all references to this Domain instance see the updated data.
        """
        # Fetch latest data from API
        response = _DOMAIN_API.get_domain(self.id)

        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self

        # Return new instance with fresh data
        return Domain(**response.model_dump())

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        in_place: bool = False,
    ) -> "Domain":
        """Update the domain's mutable properties.

        This method allows updating the name, description, and tags of a domain.
        Other properties cannot be modified - a new domain must be created instead.

        Parameters
        ----------
        name : str, optional
            New name for the domain
        description : str, optional
            New description for the domain
        tags : List[str], optional
            New list of tags for the domain
        in_place : bool, optional
            If True, updates the current Domain instance with the new data and returns
            self. If False, returns a new Domain instance with the updated data,
            leaving the current instance unchanged. Default is False.

        Returns
        -------
        Domain
            Either the current Domain instance (if in_place=True) or a new Domain
            instance (if in_place=False) containing the updated data.

        Examples
        --------
        Update and get new instance:
        >>> domain = Domain.get_domain("123")
        >>> updated = domain.update(name="New Name")  # domain remains unchanged
        >>> updated.name
        'New Name'

        Update in-place:
        >>> domain = Domain.get_domain("123")
        >>> domain.update(name="New Name", in_place=True)  # domain is modified
        >>> domain.name
        'New Name'

        Notes
        -----
        Only name, description, and tags can be updated. Other properties like
        horizontal_resolution, vertical_resolution, features, etc. cannot be
        modified - you must create a new domain instead.
        """
        # Create update request with only the fields that are provided
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if tags is not None:
            update_data["tags"] = tags

        # Only make API call if there are fields to update
        if update_data:
            request = UpdateDomainRequest(**update_data)
            response = _DOMAIN_API.update_domain(
                domain_id=self.id, update_domain_request=request
            )

            if in_place:
                # Update current instance attributes
                for key, value in response.model_dump().items():
                    setattr(self, key, value)
                return self

            # Return new instance with updated data
            return Domain(**response.model_dump())

        # If no updates, return self or new instance based on in_place
        return self if in_place else Domain(**self.model_dump())


def list_domains(
    page: Optional[int] = None,
    size: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> ListDomainResponse:
    """Retrieve a paginated list of all domains accessible to the authenticated user.

    Parameters
    ----------
    page : int, optional
        The page number to retrieve (zero-indexed). Default is 0.
    size : int, optional
        Number of domains to return per page. Must be between 1 and 1000.
        Default is 100.
    sort_by : str, optional
        Field to sort the domains by. Valid values are:
        - "createdOn"
        - "modifiedOn"
        - "name"
        Default is "createdOn".
    sort_order : str, optional
        Order in which to sort the results. Valid values are:
        - "ascending"
        - "descending"
        Default is "ascending".

    Returns
    -------
    ListDomainResponse
        A response object containing:
        - domains: List of Domain objects
        - currentPage: Current page number
        - pageSize: Number of domains per page
        - totalItems: Total number of domains available

    Examples
    --------
    Get first page with default settings:
    >>> response = list_domains()
    >>> print(f"Found {len(response.domains)} domains")

    Get specific page with custom size:
    >>> response = list_domains(page=2, size=50)
    >>> for domain in response.domains:
    ...     print(f"Domain {domain.id}: {domain.name}")

    Sort domains by name:
    >>> response = list_domains(sort_by="name", sort_order="ascending")

    Notes
    -----
    - Page numbers are zero-indexed, meaning the first page is 0.
    - If no pagination parameters are provided, defaults to page 0 with 100 items.
    - The maximum page size is 1000 items.
    - When calculating total pages, use: ceil(response.totalItems / response.pageSize)
    """
    sort_by = DomainSortField(sort_by) if sort_by else None
    sort_order = DomainSortOrder(sort_order) if sort_order else None
    list_response = _DOMAIN_API.list_domains(
        page=page, size=size, sort_by=sort_by, sort_order=sort_order
    )
    list_response.domains = [Domain(**d.model_dump()) for d in list_response.domains]
    return list_response


def get_domain(domain_id: str) -> Domain:
    """Retrieve a specific domain by its ID.

    Parameters
    ----------
    domain_id : str
        The unique identifier of the domain to retrieve.

    Returns
    -------
    Domain
        The requested domain object.

    Examples
    --------
    >>> domain = get_domain("abc123")
    >>> print(domain.name)
    "My Domain"
    >>> print(domain.horizontal_resolution)
    2.0
    """
    get_domain_response = _DOMAIN_API.get_domain(domain_id)
    return Domain(**get_domain_response.model_dump())
