from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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


T = TypeVar("T", bound="CreateCrownBaseHeightAllometryRequest")


@_attrs_define
class CreateCrownBaseHeightAllometryRequest:
    """Request body for creating an inventory with model-computed crown base
    heights.

        Attributes:
            source_tree_inventory_id (str): ID of a completed tree inventory with position and height for every tree, and
                species, dbh and crown ratio for every tree unless `model` is `gdam`.
            type_ (InventoryType | Unset): Type of entities in the inventory.
            name (str | Unset):  Default: ''.
            description (str | Unset):  Default: ''.
            tags (list[str] | Unset):
            model (FiaNationalLogit2026Model | GdamModel | Monleon2004Eq1Model | Monleon2004Eq2Model | Randolph2010Model |
                ToneyReeves2009Model | Unset | Westfall2019Model): The model that gives each tree's crown base height, selected
                by `name`. `gdam` predicts it with GDAM, conditioned on whichever of species, dbh, crown ratio and crown base
                height the tree has. The other models compute it from species, dbh, crown ratio and height; species a model does
                not cover get no crown base height.
            overwrite (bool | Unset): `false` keeps existing crown base heights and fills only empty cells. `true`
                recomputes every tree's crown base height with `model`; `gdam` is not given the old values. Default: False.
    """

    source_tree_inventory_id: str
    type_: InventoryType | Unset = UNSET
    name: str | Unset = ""
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    model: (
        FiaNationalLogit2026Model
        | GdamModel
        | Monleon2004Eq1Model
        | Monleon2004Eq2Model
        | Randolph2010Model
        | ToneyReeves2009Model
        | Unset
        | Westfall2019Model
    ) = UNSET
    overwrite: bool | Unset = False
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

        model: dict[str, Any] | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        elif (
            isinstance(self.model, FiaNationalLogit2026Model)
            or isinstance(self.model, Monleon2004Eq1Model)
            or isinstance(self.model, Monleon2004Eq2Model)
            or isinstance(self.model, ToneyReeves2009Model)
            or isinstance(self.model, Randolph2010Model)
            or isinstance(self.model, Westfall2019Model)
        ):
            model = self.model.to_dict()
        else:
            model = self.model.to_dict()

        overwrite = self.overwrite

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
        if model is not UNSET:
            field_dict["model"] = model
        if overwrite is not UNSET:
            field_dict["overwrite"] = overwrite

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

        def _parse_model(
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
                model_type_0 = FiaNationalLogit2026Model.from_dict(data)

                return model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_type_1 = Monleon2004Eq1Model.from_dict(data)

                return model_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_type_2 = Monleon2004Eq2Model.from_dict(data)

                return model_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_type_3 = ToneyReeves2009Model.from_dict(data)

                return model_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_type_4 = Randolph2010Model.from_dict(data)

                return model_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                model_type_5 = Westfall2019Model.from_dict(data)

                return model_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            model_type_6 = GdamModel.from_dict(data)

            return model_type_6

        model = _parse_model(d.pop("model", UNSET))

        overwrite = d.pop("overwrite", UNSET)

        create_crown_base_height_allometry_request = cls(
            source_tree_inventory_id=source_tree_inventory_id,
            type_=type_,
            name=name,
            description=description,
            tags=tags,
            model=model,
            overwrite=overwrite,
        )

        create_crown_base_height_allometry_request.additional_properties = d
        return create_crown_base_height_allometry_request

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
