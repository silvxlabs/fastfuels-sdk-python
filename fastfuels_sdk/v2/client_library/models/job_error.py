from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobError")


@_attrs_define
class JobError:
    """Error information for failed async jobs.

    Provides structured error information with user-facing messages and
    developer debugging information. The traceback is stored in Firestore
    but excluded from API responses.

    Attributes:
        code: Machine-readable error code for programmatic handling.
            Examples: "LANDFIRE_COVERAGE_ERROR", "SOURCE_GRID_NOT_FOUND"
        message: User-friendly explanation of what went wrong.
        suggestion: Optional actionable advice for resolving the error.
        traceback: Full Python stack trace for debugging. Stored in Firestore
            but not included in API responses.

        Attributes:
            code (str): Machine-readable error code
            message (str): User-friendly error message
            suggestion (None | str | Unset): Actionable suggestion for the user
            traceback (None | str | Unset): Full stack trace (stored but not exposed in API responses)
    """

    code: str
    message: str
    suggestion: None | str | Unset = UNSET
    traceback: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        suggestion: None | str | Unset
        if isinstance(self.suggestion, Unset):
            suggestion = UNSET
        else:
            suggestion = self.suggestion

        traceback: None | str | Unset
        if isinstance(self.traceback, Unset):
            traceback = UNSET
        else:
            traceback = self.traceback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if suggestion is not UNSET:
            field_dict["suggestion"] = suggestion
        if traceback is not UNSET:
            field_dict["traceback"] = traceback

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        def _parse_suggestion(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        suggestion = _parse_suggestion(d.pop("suggestion", UNSET))

        def _parse_traceback(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        traceback = _parse_traceback(d.pop("traceback", UNSET))

        job_error = cls(
            code=code,
            message=message,
            suggestion=suggestion,
            traceback=traceback,
        )

        job_error.additional_properties = d
        return job_error

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
