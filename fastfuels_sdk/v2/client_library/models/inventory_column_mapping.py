from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryColumnMapping")


@_attrs_define
class InventoryColumnMapping:
    """Maps v2 column names to the corresponding column names in the uploaded file.

    Omit any entry whose column already uses the v2 name. For GeoJSON and
    GeoPackage formats, x and y are extracted from geometry — their mapping
    entries are ignored.

        Attributes:
            x (None | str | Unset):
            y (None | str | Unset):
            height (None | str | Unset):
            fia_species_code (None | str | Unset):
            fia_status_code (None | str | Unset):
            fia_crown_class_code (None | str | Unset):
            dbh (None | str | Unset):
            crown_ratio (None | str | Unset):
    """

    x: None | str | Unset = UNSET
    y: None | str | Unset = UNSET
    height: None | str | Unset = UNSET
    fia_species_code: None | str | Unset = UNSET
    fia_status_code: None | str | Unset = UNSET
    fia_crown_class_code: None | str | Unset = UNSET
    dbh: None | str | Unset = UNSET
    crown_ratio: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        x: None | str | Unset
        if isinstance(self.x, Unset):
            x = UNSET
        else:
            x = self.x

        y: None | str | Unset
        if isinstance(self.y, Unset):
            y = UNSET
        else:
            y = self.y

        height: None | str | Unset
        if isinstance(self.height, Unset):
            height = UNSET
        else:
            height = self.height

        fia_species_code: None | str | Unset
        if isinstance(self.fia_species_code, Unset):
            fia_species_code = UNSET
        else:
            fia_species_code = self.fia_species_code

        fia_status_code: None | str | Unset
        if isinstance(self.fia_status_code, Unset):
            fia_status_code = UNSET
        else:
            fia_status_code = self.fia_status_code

        fia_crown_class_code: None | str | Unset
        if isinstance(self.fia_crown_class_code, Unset):
            fia_crown_class_code = UNSET
        else:
            fia_crown_class_code = self.fia_crown_class_code

        dbh: None | str | Unset
        if isinstance(self.dbh, Unset):
            dbh = UNSET
        else:
            dbh = self.dbh

        crown_ratio: None | str | Unset
        if isinstance(self.crown_ratio, Unset):
            crown_ratio = UNSET
        else:
            crown_ratio = self.crown_ratio

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y
        if height is not UNSET:
            field_dict["height"] = height
        if fia_species_code is not UNSET:
            field_dict["fia_species_code"] = fia_species_code
        if fia_status_code is not UNSET:
            field_dict["fia_status_code"] = fia_status_code
        if fia_crown_class_code is not UNSET:
            field_dict["fia_crown_class_code"] = fia_crown_class_code
        if dbh is not UNSET:
            field_dict["dbh"] = dbh
        if crown_ratio is not UNSET:
            field_dict["crown_ratio"] = crown_ratio

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_x(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        x = _parse_x(d.pop("x", UNSET))

        def _parse_y(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        y = _parse_y(d.pop("y", UNSET))

        def _parse_height(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        height = _parse_height(d.pop("height", UNSET))

        def _parse_fia_species_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fia_species_code = _parse_fia_species_code(d.pop("fia_species_code", UNSET))

        def _parse_fia_status_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fia_status_code = _parse_fia_status_code(d.pop("fia_status_code", UNSET))

        def _parse_fia_crown_class_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fia_crown_class_code = _parse_fia_crown_class_code(
            d.pop("fia_crown_class_code", UNSET)
        )

        def _parse_dbh(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dbh = _parse_dbh(d.pop("dbh", UNSET))

        def _parse_crown_ratio(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        crown_ratio = _parse_crown_ratio(d.pop("crown_ratio", UNSET))

        inventory_column_mapping = cls(
            x=x,
            y=y,
            height=height,
            fia_species_code=fia_species_code,
            fia_status_code=fia_status_code,
            fia_crown_class_code=fia_crown_class_code,
            dbh=dbh,
            crown_ratio=crown_ratio,
        )

        return inventory_column_mapping
