from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuotaExceededDetail")


@_attrs_define
class QuotaExceededDetail:
    """Structured ``detail`` for a 429 quota rejection.

    The flat ``{reason, quota, message, current, limit}`` shape is the template
    for future structured error details: a machine-readable ``reason`` code plus
    flat, typed context fields.

        Attributes:
            quota (str): The Quotas field that was exceeded.
            message (str): Human-readable explanation and next steps.
            current (int): The owner's current usage for this quota.
            limit (int): The limit that was reached.
            reason (str | Unset): Machine-readable error code. Default: 'QUOTA_EXCEEDED'.
            window_reset_on (datetime.datetime | None | Unset): When a windowed (weekly) quota resets; absent for non-
                windowed quotas.
    """

    quota: str
    message: str
    current: int
    limit: int
    reason: str | Unset = "QUOTA_EXCEEDED"
    window_reset_on: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quota = self.quota

        message = self.message

        current = self.current

        limit = self.limit

        reason = self.reason

        window_reset_on: None | str | Unset
        if isinstance(self.window_reset_on, Unset):
            window_reset_on = UNSET
        elif isinstance(self.window_reset_on, datetime.datetime):
            window_reset_on = self.window_reset_on.isoformat()
        else:
            window_reset_on = self.window_reset_on

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "quota": quota,
                "message": message,
                "current": current,
                "limit": limit,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason
        if window_reset_on is not UNSET:
            field_dict["window_reset_on"] = window_reset_on

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        quota = d.pop("quota")

        message = d.pop("message")

        current = d.pop("current")

        limit = d.pop("limit")

        reason = d.pop("reason", UNSET)

        def _parse_window_reset_on(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                window_reset_on_type_0 = datetime.datetime.fromisoformat(data)

                return window_reset_on_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        window_reset_on = _parse_window_reset_on(d.pop("window_reset_on", UNSET))

        quota_exceeded_detail = cls(
            quota=quota,
            message=message,
            current=current,
            limit=limit,
            reason=reason,
            window_reset_on=window_reset_on,
        )

        quota_exceeded_detail.additional_properties = d
        return quota_exceeded_detail

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
