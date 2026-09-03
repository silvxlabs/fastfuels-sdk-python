from __future__ import annotations

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
    from ..models.landfire_create_link_body import LandfireCreateLinkBody


T = TypeVar("T", bound="LandfireCreateLink")


@_attrs_define
class LandfireCreateLink:
    """The create request that fetches a release for this domain.

    Attributes:
        href (str): Path of the create endpoint, relative to the API base URL.
        body (LandfireCreateLinkBody): Request body selecting this release.
        method (Literal['POST'] | Unset):  Default: 'POST'.
    """

    href: str
    body: LandfireCreateLinkBody
    method: Literal["POST"] | Unset = "POST"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        body = self.body.to_dict()

        method = self.method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "href": href,
                "body": body,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.landfire_create_link_body import LandfireCreateLinkBody

        d = dict(src_dict)
        href = d.pop("href")

        body = LandfireCreateLinkBody.from_dict(d.pop("body"))

        method = cast(Literal["POST"] | Unset, d.pop("method", UNSET))
        if method != "POST" and not isinstance(method, Unset):
            raise ValueError(f"method must match const 'POST', got '{method}'")

        landfire_create_link = cls(
            href=href,
            body=body,
            method=method,
        )

        landfire_create_link.additional_properties = d
        return landfire_create_link

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
