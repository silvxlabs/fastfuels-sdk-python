"""
fastfuels_sdk/pointclouds.py
"""

# Core imports
from __future__ import annotations
from time import sleep
from typing import Optional, List

# Internal imports
from fastfuels_sdk.api import (
    get_point_cloud_api,
    get_als_point_cloud_api,
)
from fastfuels_sdk.client_library import AlsPointCloudSource
from fastfuels_sdk.utils import format_processing_error
from fastfuels_sdk.client_library.models import (
    PointCloud as PointCloudModel,
    AlsPointCloud as AlsPointCloudModel,
    CreateAlsPointCloudRequest,
)


class PointClouds(PointCloudModel):
    """Point cloud resources associated with a domain.

    Attributes
    ----------
    domain_id : str
        ID of the domain these point clouds belong to
    als : AlsPointCloud, optional
        Airborne Laser Scanning (ALS) data

    Examples
    --------
    >>> from fastfuels_sdk import PointClouds
    >>> pc = PointClouds.from_domain_id("abc123")

    >>> # Access ALS data
    >>> if pc.als:
    ...     als_data = pc.als

    >>> # Get updated point cloud data
    >>> pc = pc.get()

    See Also
    --------
    Domain : Container for point clouds
    AlsPointCloud : Airborne Laser Scanning structure
    """

    domain_id: str
    als: Optional[AlsPointCloud]

    @classmethod
    def from_domain_id(cls, domain_id: str) -> PointClouds:
        """Retrieve the point clouds associated with a domain.

        Parameters
        ----------
        domain_id : str
            The ID of the domain to retrieve point clouds for

        Returns
        -------
        PointClouds
            A PointClouds object containing:
            - als : AlsPointCloud, optional
                ALS data within the domain

        Examples
        --------
        >>> from fastfuels_sdk import PointClouds
        >>> pc = PointClouds.from_domain_id("abc123")

        >>> # Check for specific point clouds. These will be None until created.
        >>> if pc.als:
        ...     print("Domain has ALS point cloud data")

        See Also
        --------
        PointClouds.get : Refresh point cloud data
        """
        response = get_point_cloud_api().get_pointclouds(domain_id=domain_id)
        response_data = _convert_api_models_to_sdk_classes(
            domain_id, response.model_dump(), response
        )

        return cls(domain_id=domain_id, **response_data)

    def get(self, in_place: bool = False) -> PointClouds:
        """Get the latest point cloud data for this domain.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this PointClouds instance with new data.
            If False (default), returns a new PointClouds instance.

        Returns
        -------
        PointClouds
            The updated PointClouds object

        Examples
        --------
        >>> from fastfuels_sdk import PointClouds
        >>> pc = PointClouds.from_domain_id("abc123")
        >>> # Get fresh data in a new instance
        >>> updated_pc = pc.get()
        >>>
        >>> # Or update the existing instance
        >>> pc.get(in_place=True)
        """
        response = get_point_cloud_api().get_pointclouds(domain_id=self.domain_id)
        response_data = response.model_dump()
        response_data = _convert_api_models_to_sdk_classes(
            self.domain_id, response_data, response
        )

        if in_place:
            # Update all attributes of current instance
            for key, value in response_data.items():
                setattr(self, key, value)
            return self

        return PointClouds(domain_id=self.domain_id, **response_data)

    def create_als_point_cloud(
        self,
        sources: str | List[str] | AlsPointCloudSource | List[AlsPointCloudSource],
        in_place: bool = False,
    ) -> AlsPointCloud:
        """Create an ALS point cloud for this domain using specified data sources.

        Parameters
        ----------
        sources : list[str]
            Data sources to use. Supports:
            - "file": Generates a signed URL for user upload
            - "3DEP": Automatically retrieves public data (e.g. USGS 3DEP)
        in_place : bool, optional
            If True, updates this PointClouds instance with new data.
            If False (default), leaves this instance unchanged.

        Returns
        -------
        AlsPointCloud
            The newly created ALS point cloud object. If source is "file", check
            the `.file` attribute for upload URL and instructions.

        Examples
        --------
        >>> from fastfuels_sdk import PointClouds
        >>> pc = PointClouds.from_domain_id("abc123")
        >>>
        >>> # Create from public data
        >>> als = pc.create_als_point_cloud(["3DEP"])
        >>>
        >>> # Update PointClouds instance
        >>> pc.create_als_point_cloud(["3DEP"], in_place=True)
        >>> pc.als.status
        "pending"

        See Also
        --------
        AlsPointCloud.wait_until_completed : Wait for background processing
        """
        # Create API request
        request = CreateAlsPointCloudRequest(sources=sources)

        # Call API
        response = get_als_point_cloud_api().create_als_point_cloud(
            domain_id=self.domain_id, create_als_point_cloud_request=request
        )

        # Convert API model to SDK class
        als_point_cloud = AlsPointCloud(
            domain_id=self.domain_id, **response.model_dump()
        )

        if in_place:
            self.als = als_point_cloud

        return als_point_cloud


class AlsPointCloud(AlsPointCloudModel):
    """Airborne Laser Scanning (ALS) point cloud features.

    Represents high-resolution elevation data used for creating detailed canopy
    height models and tree inventories.

    Attributes
    ----------
    domain_id : str
        ID of the domain this point cloud belongs to
    sources : list[str]
        Data sources used to create these features ("file", "3DEP")
    status : str, optional
        Current processing status ("pending", "running", "completed")
    created_on : datetime, optional
        When these features were created
    modified_on : datetime, optional
        When these features were last modified
    checksum : str, optional
        Unique identifier for this version of the features
    file : dict, optional
        Contains upload instructions (URL, headers) if source is "file"

    Examples
    --------
    >>> from fastfuels_sdk import PointClouds
    >>> pc = PointClouds.from_domain_id("abc123")
    >>>
    >>> # Access existing ALS data
    >>> if pc.als:
    ...     als = pc.als
    ...     print(als.status)

    >>> # Create new ALS data
    >>> als = pc.create_als_point_cloud(["3DEP"])
    """

    domain_id: str

    def get(self, in_place: bool = False) -> AlsPointCloud:
        """Get the latest ALS point cloud data.

        Parameters
        ----------
        in_place : bool, optional
            If True, updates this AlsPointCloud instance with new data.
            If False (default), returns a new AlsPointCloud instance.

        Returns
        -------
        AlsPointCloud
            The updated ALS point cloud object

        Examples
        --------
        >>> from fastfuels_sdk import PointClouds
        >>> pc = PointClouds.from_domain_id("abc123")
        >>> als = pc.create_als_point_cloud(["3DEP"])
        >>> # Get fresh data in a new instance
        >>> updated_als = als.get()
        >>>
        >>> # Or update the existing instance
        >>> als.get(in_place=True)
        """
        response = get_als_point_cloud_api().get_als_point_cloud(
            domain_id=self.domain_id
        )
        if in_place:
            # Update all attributes of current instance
            for key, value in response.model_dump().items():
                setattr(self, key, value)
            return self
        return AlsPointCloud(domain_id=self.domain_id, **response.model_dump())

    def wait_until_completed(
        self,
        step: float = 5,
        timeout: float = 600,
        in_place: bool = True,
        verbose: bool = False,
    ) -> AlsPointCloud:
        """Wait for ALS point cloud processing to complete.

        ALS point clouds are processed asynchronously and may take several seconds
        to minutes to complete depending on domain size and data sources.

        Parameters
        ----------
        step : float, optional
            Seconds between status checks (default: 5)
        timeout : float, optional
            Maximum seconds to wait (default: 600)
        in_place : bool, optional
            If True (default), updates this instance with completed data.
            If False, returns a new instance.
        verbose : bool, optional
            If True, prints status updates (default: False)

        Returns
        -------
        AlsPointCloud
            The completed ALS point cloud object

        Examples
        --------
        >>> from fastfuels_sdk import PointClouds
        >>> pc = PointClouds.from_domain_id("abc123")
        >>> als = pc.create_als_point_cloud(["3DEP"])
        >>> als.wait_until_completed(verbose=True)
        ALS point cloud has status `pending` (5.00s)
        ALS point cloud has status `completed` (10.00s)
        """
        elapsed_time = 0
        als_point_cloud = self.get(in_place=in_place if in_place else False)
        while als_point_cloud.status != "completed":
            if als_point_cloud.status == "failed":
                error_msg = "ALS point cloud processing failed."

                # Extract detailed error information if available
                error_obj = getattr(als_point_cloud, "error", None)
                if error_obj:
                    error_details = format_processing_error(error_obj)
                    if error_details:
                        error_msg = f"{error_msg}\n\n{error_details}"

                raise RuntimeError(error_msg)
            if elapsed_time >= timeout:
                raise TimeoutError("Timed out waiting for ALS point cloud to finish.")
            sleep(step)
            elapsed_time += step
            als_point_cloud = self.get(in_place=in_place if in_place else False)
            if verbose:
                print(
                    f"ALS point cloud has status `{als_point_cloud.status}` ({elapsed_time:.2f}s)"
                )
        return als_point_cloud

    def delete(self) -> None:
        """Delete this ALS point cloud.

        Permanently removes ALS data from the domain. This also cancels
        any ongoing processing jobs and removes files from storage.

        Returns
        -------
        None

        Examples
        --------
        >>> from fastfuels_sdk import PointClouds
        >>> pc = PointClouds.from_domain_id("abc123")
        >>> als = pc.create_als_point_cloud(["3DEP"])
        >>> # Remove ALS data when no longer needed
        >>> als.delete()
        >>> # Subsequent operations will raise NotFoundException
        >>> als.get()  # raises NotFoundException
        """
        get_als_point_cloud_api().delete_als_point_cloud(domain_id=self.domain_id)
        return None


def _convert_api_models_to_sdk_classes(
    domain_id, response_data: dict, response_obj=None
) -> dict:
    """Convert API models to SDK classes with domain_id.

    Parameters
    ----------
    domain_id : str
        Domain ID to attach to point clouds
    response_data : dict
        Dict representation of the response
    response_obj : optional
        Original response object (to preserve complex nested models)
    """
    if "als" in response_data and response_data["als"]:
        response_data["als"] = AlsPointCloud(
            domain_id=domain_id, **response_data["als"]
        )

    return response_data
