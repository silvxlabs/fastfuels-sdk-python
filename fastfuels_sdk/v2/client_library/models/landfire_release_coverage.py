from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.landfire_coverage import LandfireCoverage

if TYPE_CHECKING:
    from ..models.landfire_release_links import LandfireReleaseLinks


T = TypeVar("T", bound="LandfireReleaseCoverage")


@_attrs_define
class LandfireReleaseCoverage:
    """One release of a LANDFIRE product and its coverage of the domain.

    Attributes:
        version (str): LANDFIRE landscape vintage year.
        season (None | str): LANDFIRE Seasonal Fuels window, or null for the annual product.
        year (int | None): Calendar year the data represents: the vintage for annual releases, the projected season year
            for seasonal ones. Null for a season LANDFIRE hasn't published yet.
        coverage (LandfireCoverage): How much of a domain a LANDFIRE release covers.
        links (LandfireReleaseLinks): Actions available for a release on this domain.
    """

    version: str
    season: None | str
    year: int | None
    coverage: LandfireCoverage
    links: LandfireReleaseLinks
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        season: None | str
        season = self.season

        year: int | None
        year = self.year

        coverage = self.coverage.value

        links = self.links.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "season": season,
                "year": year,
                "coverage": coverage,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.landfire_release_links import LandfireReleaseLinks

        d = dict(src_dict)
        version = d.pop("version")

        def _parse_season(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        season = _parse_season(d.pop("season"))

        def _parse_year(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        year = _parse_year(d.pop("year"))

        coverage = LandfireCoverage(d.pop("coverage"))

        links = LandfireReleaseLinks.from_dict(d.pop("links"))

        landfire_release_coverage = cls(
            version=version,
            season=season,
            year=year,
            coverage=coverage,
            links=links,
        )

        landfire_release_coverage.additional_properties = d
        return landfire_release_coverage

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
