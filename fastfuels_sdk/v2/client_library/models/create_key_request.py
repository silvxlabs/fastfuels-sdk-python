from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.access import Access
from ..models.scope import Scope
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateKeyRequest")


@_attrs_define
class CreateKeyRequest:
    """Request body for creating an API key.

    Attributes:
        name (str): A name to semantically identify the key.
        description (None | str | Unset): An optional description of the key's purpose.
        valid_days (int | Unset): Number of days for which this key will be valid. Default: 30.
        scopes (list[Scope] | Unset): A list of scopes available to the key.
        access (Access | Unset): Access types for an API key.
        application_id (None | str | Unset): Application ID accessed by the API key.
    """

    name: str
    description: None | str | Unset = UNSET
    valid_days: int | Unset = 30
    scopes: list[Scope] | Unset = UNSET
    access: Access | Unset = UNSET
    application_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

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

        access: str | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = self.access.value

        application_id: None | str | Unset
        if isinstance(self.application_id, Unset):
            application_id = UNSET
        else:
            application_id = self.application_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if valid_days is not UNSET:
            field_dict["valid_days"] = valid_days
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if access is not UNSET:
            field_dict["access"] = access
        if application_id is not UNSET:
            field_dict["application_id"] = application_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

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

        _access = d.pop("access", UNSET)
        access: Access | Unset
        if isinstance(_access, Unset):
            access = UNSET
        else:
            access = Access(_access)

        def _parse_application_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        application_id = _parse_application_id(d.pop("application_id", UNSET))

        create_key_request = cls(
            name=name,
            description=description,
            valid_days=valid_days,
            scopes=scopes,
            access=access,
            application_id=application_id,
        )

        create_key_request.additional_properties = d
        return create_key_request

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
