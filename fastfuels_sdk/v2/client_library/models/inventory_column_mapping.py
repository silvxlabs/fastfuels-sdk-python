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
            tree_id (None | str | Unset): Per-tree identifier to keep as the inventory's `tree_id`. Values must be non-null
                numbers in 1 … 2,147,483,647; they are cast to integers and must then be unique across the file; otherwise the
                upload fails with `SCHEMA_VALIDATION_ERROR`. If the file has no `tree_id` column and none is mapped, IDs 1 … N
                are generated.
            x (None | str | Unset): Tree position in the domain's projected CRS (m).
            y (None | str | Unset): Tree position in the domain's projected CRS (m).
            height (None | str | Unset): Total tree height (m).
            fia_species_code (None | str | Unset): FIA species code (SPCD).
            fia_status_code (None | str | Unset): FIA tree status code (STATUSCD): 1 live, 2 dead, 3 removed.
            fia_crown_class_code (None | str | Unset): FIA crown class code (CCLCD): 1 open-grown, 2 dominant, 3 codominant,
                4 intermediate, 5 overtopped.
            dbh (None | str | Unset): Diameter at breast height (cm).
            crown_ratio (None | str | Unset): Live crown ratio: fraction of total height with live crown (0-1).
            crown_radius (None | str | Unset): Measured crown radius (m), > 0 and <= 20. Null for trees without a
                measurement.
    """

    tree_id: None | str | Unset = UNSET
    x: None | str | Unset = UNSET
    y: None | str | Unset = UNSET
    height: None | str | Unset = UNSET
    fia_species_code: None | str | Unset = UNSET
    fia_status_code: None | str | Unset = UNSET
    fia_crown_class_code: None | str | Unset = UNSET
    dbh: None | str | Unset = UNSET
    crown_ratio: None | str | Unset = UNSET
    crown_radius: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        tree_id: None | str | Unset
        if isinstance(self.tree_id, Unset):
            tree_id = UNSET
        else:
            tree_id = self.tree_id

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

        crown_radius: None | str | Unset
        if isinstance(self.crown_radius, Unset):
            crown_radius = UNSET
        else:
            crown_radius = self.crown_radius

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if tree_id is not UNSET:
            field_dict["tree_id"] = tree_id
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
        if crown_radius is not UNSET:
            field_dict["crown_radius"] = crown_radius

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_tree_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tree_id = _parse_tree_id(d.pop("tree_id", UNSET))

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

        def _parse_crown_radius(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        crown_radius = _parse_crown_radius(d.pop("crown_radius", UNSET))

        inventory_column_mapping = cls(
            tree_id=tree_id,
            x=x,
            y=y,
            height=height,
            fia_species_code=fia_species_code,
            fia_status_code=fia_status_code,
            fia_crown_class_code=fia_crown_class_code,
            dbh=dbh,
            crown_ratio=crown_ratio,
            crown_radius=crown_radius,
        )

        return inventory_column_mapping
