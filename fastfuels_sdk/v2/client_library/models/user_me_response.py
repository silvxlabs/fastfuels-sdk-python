from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_me_response_kind import UserMeResponseKind

if TYPE_CHECKING:
    from ..models.quotas import Quotas


T = TypeVar("T", bound="UserMeResponse")


@_attrs_define
class UserMeResponse:
    """The authenticated owner's identity and resolved quota configuration.

    Attributes:
        id (str): The authenticated owner's unique ID.
        kind (UserMeResponseKind): Whether the credential authenticated a user or an application.
        tier (str): The quota tier in effect for this owner.
        quotas (Quotas): Usage limits for an owner. Field defaults are the standard tier.
    """

    id: str
    kind: UserMeResponseKind
    tier: str
    quotas: Quotas
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        kind = self.kind.value

        tier = self.tier

        quotas = self.quotas.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "tier": tier,
                "quotas": quotas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.quotas import Quotas

        d = dict(src_dict)
        id = d.pop("id")

        kind = UserMeResponseKind(d.pop("kind"))

        tier = d.pop("tier")

        quotas = Quotas.from_dict(d.pop("quotas"))

        user_me_response = cls(
            id=id,
            kind=kind,
            tier=tier,
            quotas=quotas,
        )

        user_me_response.additional_properties = d
        return user_me_response

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
