from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.landfire_release_coverage import LandfireReleaseCoverage


T = TypeVar("T", bound="LandfireCoverageResponse")


@_attrs_define
class LandfireCoverageResponse:
    """Response model for the LANDFIRE release coverage pre-flight check.

    Attributes:
        product (str):
        latest (LandfireReleaseCoverage | None): The release representing the most recent point in time that fully
            covers the domain. Null when none does.
        releases (list[LandfireReleaseCoverage]): Every release the API serves, newest first by the time the data
            represents. Seasons LANDFIRE hasn't published yet are listed where they will land once published.
    """

    product: str
    latest: LandfireReleaseCoverage | None
    releases: list[LandfireReleaseCoverage]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.landfire_release_coverage import LandfireReleaseCoverage

        product = self.product

        latest: dict[str, Any] | None
        if isinstance(self.latest, LandfireReleaseCoverage):
            latest = self.latest.to_dict()
        else:
            latest = self.latest

        releases = []
        for releases_item_data in self.releases:
            releases_item = releases_item_data.to_dict()
            releases.append(releases_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "product": product,
                "latest": latest,
                "releases": releases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.landfire_release_coverage import LandfireReleaseCoverage

        d = dict(src_dict)
        product = d.pop("product")

        def _parse_latest(data: object) -> LandfireReleaseCoverage | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_type_0 = LandfireReleaseCoverage.from_dict(data)

                return latest_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LandfireReleaseCoverage | None, data)

        latest = _parse_latest(d.pop("latest"))

        releases = []
        _releases = d.pop("releases")
        for releases_item_data in _releases:
            releases_item = LandfireReleaseCoverage.from_dict(releases_item_data)

            releases.append(releases_item)

        landfire_coverage_response = cls(
            product=product,
            latest=latest,
            releases=releases,
        )

        landfire_coverage_response.additional_properties = d
        return landfire_coverage_response

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
