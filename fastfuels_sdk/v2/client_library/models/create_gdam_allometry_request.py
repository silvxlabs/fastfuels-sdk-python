from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_gdam_allometry_request_impute_columns_item import (
    CreateGdamAllometryRequestImputeColumnsItem,
)
from ..models.inventory_type import InventoryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fia_national_logit_2026_model import FiaNationalLogit2026Model
    from ..models.gdam_model import GdamModel
    from ..models.monleon_2004_eq_1_model import Monleon2004Eq1Model
    from ..models.monleon_2004_eq_2_model import Monleon2004Eq2Model
    from ..models.randolph_2010_model import Randolph2010Model
    from ..models.toney_reeves_2009_model import ToneyReeves2009Model
    from ..models.westfall_2019_model import Westfall2019Model


T = TypeVar("T", bound="CreateGdamAllometryRequest")


@_attrs_define
class CreateGdamAllometryRequest:
    """Request body for creating an inventory via GDAM allometry imputation.

    Attributes:
        source_tree_inventory_id (str): ID of a completed tree inventory whose morphology columns (dbh, crown ratio,
            species, crown base height) will be filled in.
        type_ (InventoryType | Unset): Type of entities in the inventory.
        name (str | Unset):  Default: ''.
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        impute_columns (list[CreateGdamAllometryRequestImputeColumnsItem] | Unset): Which morphology columns to impute.
            Defaults to all of `dbh`, `crown_ratio`, `fia_species_code`, `crown_base_height`. Narrow it (e.g.
            `['fia_species_code']`) to impute fewer columns and write less to disk; columns left out are not imputed (they
            stay as the source had them). GDAM predicts `dbh`, `crown_ratio` and `fia_species_code`, and `crown_base_height`
            with the `gdam` `crown_base_height_model`. Any other model computes `crown_base_height` from those and `height`,
            so each of them must be imputed too or be a column of the source inventory, and with `overwrite`, replacing
            `crown_ratio` without `crown_base_height` leaves crown bases that no longer match the new crown ratios. Must
            contain at least one column, with no duplicates.
        overwrite (bool | Unset): `false` keeps existing values and fills only empty cells of `impute_columns`. `true`
            replaces every tree's value in `impute_columns`; the old values are not given to GDAM. Default: False.
        crown_base_height_model (FiaNationalLogit2026Model | GdamModel | Monleon2004Eq1Model | Monleon2004Eq2Model |
            Randolph2010Model | ToneyReeves2009Model | Unset | Westfall2019Model): The model that gives `crown_base_height`.
            `gdam` (the default) predicts it with the other columns; any other model computes it from each tree's species,
            dbh, crown ratio and height after GDAM fills them.
    """

    source_tree_inventory_id: str
    type_: InventoryType | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    impute_columns: list[CreateGdamAllometryRequestImputeColumnsItem] | Unset = UNSET
    overwrite: bool | Unset = False
    crown_base_height_model: (
        FiaNationalLogit2026Model
        | GdamModel
        | Monleon2004Eq1Model
        | Monleon2004Eq2Model
        | Randolph2010Model
        | ToneyReeves2009Model
        | Unset
        | Westfall2019Model
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fia_national_logit_2026_model import FiaNationalLogit2026Model
        from ..models.monleon_2004_eq_1_model import Monleon2004Eq1Model
        from ..models.monleon_2004_eq_2_model import Monleon2004Eq2Model
        from ..models.randolph_2010_model import Randolph2010Model
        from ..models.toney_reeves_2009_model import ToneyReeves2009Model
        from ..models.westfall_2019_model import Westfall2019Model

        source_tree_inventory_id = self.source_tree_inventory_id

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        impute_columns: list[str] | Unset = UNSET
        if not isinstance(self.impute_columns, Unset):
            impute_columns = []
            for impute_columns_item_data in self.impute_columns:
                impute_columns_item = impute_columns_item_data.value
                impute_columns.append(impute_columns_item)

        overwrite = self.overwrite

        crown_base_height_model: dict[str, Any] | Unset
        if isinstance(self.crown_base_height_model, Unset):
            crown_base_height_model = UNSET
        elif (
            isinstance(self.crown_base_height_model, FiaNationalLogit2026Model)
            or isinstance(self.crown_base_height_model, Monleon2004Eq1Model)
            or isinstance(self.crown_base_height_model, Monleon2004Eq2Model)
            or isinstance(self.crown_base_height_model, ToneyReeves2009Model)
            or isinstance(self.crown_base_height_model, Randolph2010Model)
            or isinstance(self.crown_base_height_model, Westfall2019Model)
        ):
            crown_base_height_model = self.crown_base_height_model.to_dict()
        else:
            crown_base_height_model = self.crown_base_height_model.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_tree_inventory_id": source_tree_inventory_id,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if impute_columns is not UNSET:
            field_dict["impute_columns"] = impute_columns
        if overwrite is not UNSET:
            field_dict["overwrite"] = overwrite
        if crown_base_height_model is not UNSET:
            field_dict["crown_base_height_model"] = crown_base_height_model

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.fia_national_logit_2026_model import FiaNationalLogit2026Model
        from ..models.gdam_model import GdamModel
        from ..models.monleon_2004_eq_1_model import Monleon2004Eq1Model
        from ..models.monleon_2004_eq_2_model import Monleon2004Eq2Model
        from ..models.randolph_2010_model import Randolph2010Model
        from ..models.toney_reeves_2009_model import ToneyReeves2009Model
        from ..models.westfall_2019_model import Westfall2019Model

        d = dict(src_dict)
        source_tree_inventory_id = d.pop("source_tree_inventory_id")

        _type_ = d.pop("type", UNSET)
        type_: InventoryType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = InventoryType(_type_)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _impute_columns = d.pop("impute_columns", UNSET)
        impute_columns: list[CreateGdamAllometryRequestImputeColumnsItem] | Unset = (
            UNSET
        )
        if _impute_columns is not UNSET:
            impute_columns = []
            for impute_columns_item_data in _impute_columns:
                impute_columns_item = CreateGdamAllometryRequestImputeColumnsItem(
                    impute_columns_item_data
                )

                impute_columns.append(impute_columns_item)

        overwrite = d.pop("overwrite", UNSET)

        def _parse_crown_base_height_model(
            data: object,
        ) -> (
            FiaNationalLogit2026Model
            | GdamModel
            | Monleon2004Eq1Model
            | Monleon2004Eq2Model
            | Randolph2010Model
            | ToneyReeves2009Model
            | Unset
            | Westfall2019Model
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_base_height_model_type_0 = FiaNationalLogit2026Model.from_dict(
                    data
                )

                return crown_base_height_model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_base_height_model_type_1 = Monleon2004Eq1Model.from_dict(data)

                return crown_base_height_model_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_base_height_model_type_2 = Monleon2004Eq2Model.from_dict(data)

                return crown_base_height_model_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_base_height_model_type_3 = ToneyReeves2009Model.from_dict(data)

                return crown_base_height_model_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_base_height_model_type_4 = Randolph2010Model.from_dict(data)

                return crown_base_height_model_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                crown_base_height_model_type_5 = Westfall2019Model.from_dict(data)

                return crown_base_height_model_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            crown_base_height_model_type_6 = GdamModel.from_dict(data)

            return crown_base_height_model_type_6

        crown_base_height_model = _parse_crown_base_height_model(
            d.pop("crown_base_height_model", UNSET)
        )

        create_gdam_allometry_request = cls(
            source_tree_inventory_id=source_tree_inventory_id,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            impute_columns=impute_columns,
            overwrite=overwrite,
            crown_base_height_model=crown_base_height_model,
        )

        create_gdam_allometry_request.additional_properties = d
        return create_gdam_allometry_request

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
