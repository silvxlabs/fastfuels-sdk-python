from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.upload_band_definition import UploadBandDefinition


T = TypeVar("T", bound="CreateGeoTIFFUploadRequest")


@_attrs_define
class CreateGeoTIFFUploadRequest:
    """
    Attributes:
        bands (list[UploadBandDefinition]):
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        num_buffer_cells (int | Unset): Number of extra native-resolution cells to keep around the domain extent in the
            stored grid. The uploaded GeoTIFF must cover the domain bbox expanded by num_buffer_cells * native_pixel_size on
            each side; pixels beyond that expanded extent are clipped away. Default: 0.
    """

    bands: list[UploadBandDefinition]
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    num_buffer_cells: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bands = []
        for bands_item_data in self.bands:
            bands_item = bands_item_data.to_dict()
            bands.append(bands_item)

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        num_buffer_cells = self.num_buffer_cells

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bands": bands,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if num_buffer_cells is not UNSET:
            field_dict["num_buffer_cells"] = num_buffer_cells

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.upload_band_definition import UploadBandDefinition

        d = dict(src_dict)
        bands = []
        _bands = d.pop("bands")
        for bands_item_data in _bands:
            bands_item = UploadBandDefinition.from_dict(bands_item_data)

            bands.append(bands_item)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        num_buffer_cells = d.pop("num_buffer_cells", UNSET)

        create_geo_tiff_upload_request = cls(
            bands=bands,
            name=name,
            description=description,
            tags=tags,
            num_buffer_cells=num_buffer_cells,
        )

        create_geo_tiff_upload_request.additional_properties = d
        return create_geo_tiff_upload_request

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
