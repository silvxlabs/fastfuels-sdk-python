from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.point_cloud_type import PointCloudType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatePointCloudUploadRequest")


@_attrs_define
class CreatePointCloudUploadRequest:
    """Request body for creating a point cloud from a direct file upload.

    Attributes:
        type_ (PointCloudType): How a point cloud was acquired.

            The acquisition platform determines the cloud's geometry and which downstream
            products it can feed, so it is recorded as a first-class, filterable field.

            - ``als`` — **Airborne Laser Scanning.** Captured from an aircraft or drone
              looking down. Covers large areas from above and is the basis for canopy
              height models and individual-tree detection. Available from an upload or
              from USGS 3DEP.
            - ``tls`` — **Terrestrial Laser Scanning.** Captured from a tripod-mounted
              scanner on the ground looking out and up. Resolves fine sub-canopy and
              stem structure over a small plot. Available from an upload only (3DEP is
              airborne and cannot produce terrestrial scans).
        name (str | Unset): Human-readable name for the point cloud. Default: ''.
        description (str | Unset): Longer free-text description of the point cloud. Default: ''.
        tags (list[str] | Unset): Tags for organizing and filtering point clouds.
    """

    type_: PointCloudType
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        type_ = PointCloudType(d.pop("type"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        create_point_cloud_upload_request = cls(
            type_=type_,
            name=name,
            description=description,
            tags=tags,
        )

        create_point_cloud_upload_request.additional_properties = d
        return create_point_cloud_upload_request

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
