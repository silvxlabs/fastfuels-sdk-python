from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateApplicationKeyRequest")


@_attrs_define
class CreateApplicationKeyRequest:
    """Request body for a key that acts as one of your applications.

    Attributes:
        name (str): A name to semantically identify the key.
        access (Literal['application']): Access type for the API key.
        application_id (str): Application ID accessed by the API key.
        description (None | str | Unset): An optional description of the key's purpose.
        valid_days (int | Unset): Number of days for which this key will be valid. Default: 30.
        scopes (list[Scope] | Unset): A list of scopes available to the key.
    """

    name: str
    access: Literal["application"]
    application_id: str
    description: None | str | Unset = UNSET
    valid_days: int | Unset = 30
    scopes: list[Scope] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        access = self.access

        application_id = self.application_id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        valid_days = self.valid_days

        scopes: list[str] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = []
            for scopes_item_data in self.scopes:
                scopes_item = scopes_item_data.value
                scopes.append(scopes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "access": access,
                "application_id": application_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if valid_days is not UNSET:
            field_dict["valid_days"] = valid_days
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        access = cast(Literal["application"], d.pop("access"))
        if access != "application":
            raise ValueError(f"access must match const 'application', got '{access}'")

        application_id = d.pop("application_id")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        valid_days = d.pop("valid_days", UNSET)

        _scopes = d.pop("scopes", UNSET)
        scopes: list[Scope] | Unset = UNSET
        if _scopes is not UNSET:
            scopes = []
            for scopes_item_data in _scopes:
                scopes_item = Scope(scopes_item_data)

                scopes.append(scopes_item)

        create_application_key_request = cls(
            name=name,
            access=access,
            application_id=application_id,
            description=description,
            valid_days=valid_days,
            scopes=scopes,
        )

        create_application_key_request.additional_properties = d
        return create_application_key_request

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
