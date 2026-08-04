from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateThreeDepPointCloudRequest")


@_attrs_define
class CreateThreeDepPointCloudRequest:
    """Request body for fetching a point cloud from USGS 3DEP.

    Attributes:
        name (str | Unset): Human-readable name for the point cloud. Default: ''.
        description (str | Unset): Longer free-text description of the point cloud. Default: ''.
        tags (list[str] | Unset): Tags for organizing and filtering point clouds.
        datasets (list[str] | None | Unset): Names of the 3DEP acquisitions to read, in priority order. Omit this to let
            the backend choose, which it does by preferring a single acquisition that covers the whole domain and otherwise
            combining the fewest acquisitions that fill it. Set it to pin the result to specific acquisitions — for example
            to force a higher-density or more recent survey where several overlap. Where two listed acquisitions overlap,
            the one listed first is used. Names come from the coverage endpoint; every name must exist and overlap the
            domain.
    """

    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    datasets: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        datasets: list[str] | None | Unset
        if isinstance(self.datasets, Unset):
            datasets = UNSET
        elif isinstance(self.datasets, list):
            datasets = self.datasets

        else:
            datasets = self.datasets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if datasets is not UNSET:
            field_dict["datasets"] = datasets

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_datasets(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                datasets_type_0 = cast(list[str], data)

                return datasets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        datasets = _parse_datasets(d.pop("datasets", UNSET))

        create_three_dep_point_cloud_request = cls(
            name=name,
            description=description,
            tags=tags,
            datasets=datasets,
        )

        create_three_dep_point_cloud_request.additional_properties = d
        return create_three_dep_point_cloud_request

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
