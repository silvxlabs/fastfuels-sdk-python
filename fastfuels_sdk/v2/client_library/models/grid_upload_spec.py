from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GridUploadSpec")


@_attrs_define
class GridUploadSpec:
    """
    Attributes:
        url (str):
        content_type (str):
        expires_at (datetime.datetime):
        max_size_bytes (int):
        method (Literal['PUT'] | Unset):  Default: 'PUT'.
    """

    url: str
    content_type: str
    expires_at: datetime.datetime
    max_size_bytes: int
    method: Literal["PUT"] | Unset = "PUT"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        content_type = self.content_type

        expires_at = self.expires_at.isoformat()

        max_size_bytes = self.max_size_bytes

        method = self.method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "content_type": content_type,
                "expires_at": expires_at,
                "max_size_bytes": max_size_bytes,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        content_type = d.pop("content_type")

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        max_size_bytes = d.pop("max_size_bytes")

        method = cast(Literal["PUT"] | Unset, d.pop("method", UNSET))
        if method != "PUT" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'PUT', got '{method}'")

        grid_upload_spec = cls(
            url=url,
            content_type=content_type,
            expires_at=expires_at,
            max_size_bytes=max_size_bytes,
            method=method,
        )

        grid_upload_spec.additional_properties = d
        return grid_upload_spec

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
