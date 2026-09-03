from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.landfire_create_link import LandfireCreateLink


T = TypeVar("T", bound="LandfireReleaseLinks")


@_attrs_define
class LandfireReleaseLinks:
    """Actions available for a release on this domain.

    Attributes:
        create (LandfireCreateLink | None): Request that creates a grid from this release. Null when the release doesn't
            cover the domain, so the create would be rejected.
    """

    create: LandfireCreateLink | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.landfire_create_link import LandfireCreateLink

        create: dict[str, Any] | None
        if isinstance(self.create, LandfireCreateLink):
            create = self.create.to_dict()
        else:
            create = self.create

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "create": create,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.landfire_create_link import LandfireCreateLink

        d = dict(src_dict)

        def _parse_create(data: object) -> LandfireCreateLink | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                create_type_0 = LandfireCreateLink.from_dict(data)

                return create_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LandfireCreateLink | None, data)

        create = _parse_create(d.pop("create"))

        landfire_release_links = cls(
            create=create,
        )

        landfire_release_links.additional_properties = d
        return landfire_release_links

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
