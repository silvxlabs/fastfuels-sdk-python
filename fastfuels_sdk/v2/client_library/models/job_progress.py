from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobProgress")


@_attrs_define
class JobProgress:
    """Progress information for running async jobs.

    Provides real-time feedback during long-running operations.

    Attributes:
        percent: Completion percentage (0-100). Null for indeterminate operations
            like "Connecting to LANDFIRE..." where progress can't be quantified.
        message: Human-readable status message describing what's happening.

        Attributes:
            message (str): Human-readable status message, e.g. 'Fetching LANDFIRE data...'
            percent (int | None | Unset): Completion percentage (0-100), null if indeterminate
    """

    message: str
    percent: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        percent: int | None | Unset
        if isinstance(self.percent, Unset):
            percent = UNSET
        else:
            percent = self.percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if percent is not UNSET:
            field_dict["percent"] = percent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        def _parse_percent(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        percent = _parse_percent(d.pop("percent", UNSET))

        job_progress = cls(
            message=message,
            percent=percent,
        )

        job_progress.additional_properties = d
        return job_progress

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
