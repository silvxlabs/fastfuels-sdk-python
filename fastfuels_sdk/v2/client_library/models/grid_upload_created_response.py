from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.grid import Grid
    from ..models.grid_upload_spec import GridUploadSpec


T = TypeVar("T", bound="GridUploadCreatedResponse")


@_attrs_define
class GridUploadCreatedResponse:
    """
    Attributes:
        grid (Grid): The Grid resource.

            When status is "pending" or "running", georeference will be null.
            The backend populates georeference after successfully fetching data,
            at which point status transitions to "completed".

            When status is "failed", the error field contains details about what
            went wrong and suggestions for the user. The full traceback is stored
            in Firestore but not exposed in API responses.
        upload (GridUploadSpec):
    """

    grid: Grid
    upload: GridUploadSpec
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grid = self.grid.to_dict()

        upload = self.upload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grid": grid,
                "upload": upload,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.grid import Grid
        from ..models.grid_upload_spec import GridUploadSpec

        d = dict(src_dict)
        grid = Grid.from_dict(d.pop("grid"))

        upload = GridUploadSpec.from_dict(d.pop("upload"))

        grid_upload_created_response = cls(
            grid=grid,
            upload=upload,
        )

        grid_upload_created_response.additional_properties = d
        return grid_upload_created_response

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
