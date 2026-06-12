from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.point_cloud import PointCloud
    from ..models.point_cloud_upload_spec import PointCloudUploadSpec


T = TypeVar("T", bound="PointCloudUploadCreatedResponse")


@_attrs_define
class PointCloudUploadCreatedResponse:
    """Response returned when a point cloud upload is created.

    Attributes:
        point_cloud (PointCloud): A laser-scanned point cloud scoped to a single domain.

            Point clouds are created asynchronously: a creation request returns
            immediately with ``status="pending"`` and the file is ingested in the
            background. While ``status`` is ``"pending"`` or ``"running"`` the
            derived fields (`georeference`) are ``null``; the backend fills them in once
            ingestion succeeds and flips ``status`` to ``"completed"``. If ingestion
            fails, ``status`` becomes ``"failed"`` and `error` explains why.

            A completed point cloud is an input you compose with other resources — most
            directly, an ALS cloud feeds a canopy-height-model grid, which feeds a tree
            inventory.
        upload (PointCloudUploadSpec): Where and how to upload the source file.

            PUT the file to `url`, sending every header in `headers` exactly as given.
            The upload must complete before `expires_at` and must not exceed
            `max_size_bytes`.
    """

    point_cloud: PointCloud
    upload: PointCloudUploadSpec
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        point_cloud = self.point_cloud.to_dict()

        upload = self.upload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "point_cloud": point_cloud,
                "upload": upload,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.point_cloud import PointCloud
        from ..models.point_cloud_upload_spec import PointCloudUploadSpec

        d = dict(src_dict)
        point_cloud = PointCloud.from_dict(d.pop("point_cloud"))

        upload = PointCloudUploadSpec.from_dict(d.pop("upload"))

        point_cloud_upload_created_response = cls(
            point_cloud=point_cloud,
            upload=upload,
        )

        point_cloud_upload_created_response.additional_properties = d
        return point_cloud_upload_created_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
