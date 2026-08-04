from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.application_quota_overrides_type_0 import (
        ApplicationQuotaOverridesType0,
    )


T = TypeVar("T", bound="Application")


@_attrs_define
class Application:
    """Represents an application that can own API keys.

    Attributes:
        id (str): Unique identifier for the application.
        owner_id (str): The unique ID of the user who owns the application.
        name (str): Name of the application.
        description (None | str | Unset): Description of the application.
        created_on (datetime.datetime | Unset): When the application was created.
        modified_on (datetime.datetime | Unset): When the application was last modified.
        tier (None | str | Unset): Quota tier for the application. Set by the FastFuels team.
        quota_overrides (ApplicationQuotaOverridesType0 | None | Unset): Per-application quota overrides. Set by the
            FastFuels team.
    """

    id: str
    owner_id: str
    name: str
    description: None | str | Unset = UNSET
    created_on: datetime.datetime | Unset = UNSET
    modified_on: datetime.datetime | Unset = UNSET
    tier: None | str | Unset = UNSET
    quota_overrides: ApplicationQuotaOverridesType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.application_quota_overrides_type_0 import (
            ApplicationQuotaOverridesType0,
        )

        id = self.id

        owner_id = self.owner_id

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        created_on: str | Unset = UNSET
        if not isinstance(self.created_on, Unset):
            created_on = self.created_on.isoformat()

        modified_on: str | Unset = UNSET
        if not isinstance(self.modified_on, Unset):
            modified_on = self.modified_on.isoformat()

        tier: None | str | Unset
        if isinstance(self.tier, Unset):
            tier = UNSET
        else:
            tier = self.tier

        quota_overrides: dict[str, Any] | None | Unset
        if isinstance(self.quota_overrides, Unset):
            quota_overrides = UNSET
        elif isinstance(self.quota_overrides, ApplicationQuotaOverridesType0):
            quota_overrides = self.quota_overrides.to_dict()
        else:
            quota_overrides = self.quota_overrides

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "owner_id": owner_id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if created_on is not UNSET:
            field_dict["created_on"] = created_on
        if modified_on is not UNSET:
            field_dict["modified_on"] = modified_on
        if tier is not UNSET:
            field_dict["tier"] = tier
        if quota_overrides is not UNSET:
            field_dict["quota_overrides"] = quota_overrides

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.application_quota_overrides_type_0 import (
            ApplicationQuotaOverridesType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        owner_id = d.pop("owner_id")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _created_on = d.pop("created_on", UNSET)
        created_on: datetime.datetime | Unset
        if isinstance(_created_on, Unset):
            created_on = UNSET
        else:
            created_on = datetime.datetime.fromisoformat(_created_on)

        _modified_on = d.pop("modified_on", UNSET)
        modified_on: datetime.datetime | Unset
        if isinstance(_modified_on, Unset):
            modified_on = UNSET
        else:
            modified_on = datetime.datetime.fromisoformat(_modified_on)

        def _parse_tier(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tier = _parse_tier(d.pop("tier", UNSET))

        def _parse_quota_overrides(
            data: object,
        ) -> ApplicationQuotaOverridesType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                quota_overrides_type_0 = ApplicationQuotaOverridesType0.from_dict(data)

                return quota_overrides_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ApplicationQuotaOverridesType0 | None | Unset, data)

        quota_overrides = _parse_quota_overrides(d.pop("quota_overrides", UNSET))

        application = cls(
            id=id,
            owner_id=owner_id,
            name=name,
            description=description,
            created_on=created_on,
            modified_on=modified_on,
            tier=tier,
            quota_overrides=quota_overrides,
        )

        application.additional_properties = d
        return application

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
