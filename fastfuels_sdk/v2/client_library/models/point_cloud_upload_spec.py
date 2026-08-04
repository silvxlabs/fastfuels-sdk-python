from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.point_cloud_upload_spec_headers import PointCloudUploadSpecHeaders


T = TypeVar("T", bound="PointCloudUploadSpec")


@_attrs_define
class PointCloudUploadSpec:
    """Where and how to upload the source file.

    PUT the file to `url`, sending every header in `headers` exactly as given.
    The upload must complete before `expires_at` and must not exceed
    `max_size_bytes`.

        Attributes:
            url (str): Signed URL to upload the source file to.
            headers (PointCloudUploadSpecHeaders): HTTP headers that must be sent with the PUT request, exactly as given.
                The signed URL commits to these headers; the upload is rejected if any is missing or altered.
            content_type (str): Value the `Content-Type` header must use when uploading.
            expires_at (datetime.datetime): When the signed URL expires.
            max_size_bytes (int): Maximum allowed size of the uploaded file, in bytes.
            method (Literal['PUT'] | Unset):  Default: 'PUT'.
    """

    url: str
    headers: PointCloudUploadSpecHeaders
    content_type: str
    expires_at: datetime.datetime
    max_size_bytes: int
    method: Literal["PUT"] | Unset = "PUT"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        headers = self.headers.to_dict()

        content_type = self.content_type

        expires_at = self.expires_at.isoformat()

        max_size_bytes = self.max_size_bytes

        method = self.method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "headers": headers,
                "content_type": content_type,
                "expires_at": expires_at,
                "max_size_bytes": max_size_bytes,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.point_cloud_upload_spec_headers import PointCloudUploadSpecHeaders

        d = dict(src_dict)
        url = d.pop("url")

        headers = PointCloudUploadSpecHeaders.from_dict(d.pop("headers"))

        content_type = d.pop("content_type")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        max_size_bytes = d.pop("max_size_bytes")

        method = cast(Literal["PUT"] | Unset, d.pop("method", UNSET))
        if method != "PUT" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'PUT', got '{method}'")

        point_cloud_upload_spec = cls(
            url=url,
            headers=headers,
            content_type=content_type,
            expires_at=expires_at,
            max_size_bytes=max_size_bytes,
            method=method,
        )

        point_cloud_upload_spec.additional_properties = d
        return point_cloud_upload_spec

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
