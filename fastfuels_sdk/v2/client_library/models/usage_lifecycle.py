from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageLifecycle")


@_attrs_define
class UsageLifecycle:
    """Retention policy in effect for the owner's resources.

    Attributes:
        resource_ttl_days (int | None): Days a resource is retained after last modification; null never expires.
        failed_resource_ttl_days (int | None): Shorter retention for failed resources; null never expires.
        next_expiry_on (datetime.datetime | None | Unset): When the owner's next resource is scheduled to expire.
            Populated once retention enforcement ships.
    """

    resource_ttl_days: int | None
    failed_resource_ttl_days: int | None
    next_expiry_on: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_ttl_days: int | None
        resource_ttl_days = self.resource_ttl_days

        failed_resource_ttl_days: int | None
        failed_resource_ttl_days = self.failed_resource_ttl_days

        next_expiry_on: None | str | Unset
        if isinstance(self.next_expiry_on, Unset):
            next_expiry_on = UNSET
        elif isinstance(self.next_expiry_on, datetime.datetime):
            next_expiry_on = self.next_expiry_on.isoformat()
        else:
            next_expiry_on = self.next_expiry_on

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_ttl_days": resource_ttl_days,
                "failed_resource_ttl_days": failed_resource_ttl_days,
            }
        )
        if next_expiry_on is not UNSET:
            field_dict["next_expiry_on"] = next_expiry_on

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_resource_ttl_days(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        resource_ttl_days = _parse_resource_ttl_days(d.pop("resource_ttl_days"))

        def _parse_failed_resource_ttl_days(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        failed_resource_ttl_days = _parse_failed_resource_ttl_days(
            d.pop("failed_resource_ttl_days")
        )

        def _parse_next_expiry_on(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_expiry_on_type_0 = datetime.datetime.fromisoformat(data)

                return next_expiry_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        next_expiry_on = _parse_next_expiry_on(d.pop("next_expiry_on", UNSET))

        usage_lifecycle = cls(
            resource_ttl_days=resource_ttl_days,
            failed_resource_ttl_days=failed_resource_ttl_days,
            next_expiry_on=next_expiry_on,
        )

        usage_lifecycle.additional_properties = d
        return usage_lifecycle

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
