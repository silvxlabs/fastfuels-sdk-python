from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.count_usage import CountUsage
    from ..models.job_resource_usage import JobResourceUsage
    from ..models.usage_lifecycle import UsageLifecycle


T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """An owner's current usage against their resolved limits.

    Attributes:
        grids (JobResourceUsage): Usage for a resource type that produces jobs and stores artifacts.
        exports (JobResourceUsage): Usage for a resource type that produces jobs and stores artifacts.
        inventories (JobResourceUsage): Usage for a resource type that produces jobs and stores artifacts.
        features (JobResourceUsage): Usage for a resource type that produces jobs and stores artifacts.
        pointclouds (JobResourceUsage): Usage for a resource type that produces jobs and stores artifacts.
        domains (CountUsage): Usage for a count-only resource type (domains, applications, API keys).
        applications (CountUsage): Usage for a count-only resource type (domains, applications, API keys).
        api_keys (CountUsage): Usage for a count-only resource type (domains, applications, API keys).
        lifecycle (UsageLifecycle): Retention policy in effect for the owner's resources.
    """

    grids: JobResourceUsage
    exports: JobResourceUsage
    inventories: JobResourceUsage
    features: JobResourceUsage
    pointclouds: JobResourceUsage
    domains: CountUsage
    applications: CountUsage
    api_keys: CountUsage
    lifecycle: UsageLifecycle
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grids = self.grids.to_dict()

        exports = self.exports.to_dict()

        inventories = self.inventories.to_dict()

        features = self.features.to_dict()

        pointclouds = self.pointclouds.to_dict()

        domains = self.domains.to_dict()

        applications = self.applications.to_dict()

        api_keys = self.api_keys.to_dict()

        lifecycle = self.lifecycle.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grids": grids,
                "exports": exports,
                "inventories": inventories,
                "features": features,
                "pointclouds": pointclouds,
                "domains": domains,
                "applications": applications,
                "api_keys": api_keys,
                "lifecycle": lifecycle,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.count_usage import CountUsage
        from ..models.job_resource_usage import JobResourceUsage
        from ..models.usage_lifecycle import UsageLifecycle

        d = dict(src_dict)
        grids = JobResourceUsage.from_dict(d.pop("grids"))

        exports = JobResourceUsage.from_dict(d.pop("exports"))

        inventories = JobResourceUsage.from_dict(d.pop("inventories"))

        features = JobResourceUsage.from_dict(d.pop("features"))

        pointclouds = JobResourceUsage.from_dict(d.pop("pointclouds"))

        domains = CountUsage.from_dict(d.pop("domains"))

        applications = CountUsage.from_dict(d.pop("applications"))

        api_keys = CountUsage.from_dict(d.pop("api_keys"))

        lifecycle = UsageLifecycle.from_dict(d.pop("lifecycle"))

        usage = cls(
            grids=grids,
            exports=exports,
            inventories=inventories,
            features=features,
            pointclouds=pointclouds,
            domains=domains,
            applications=applications,
            api_keys=api_keys,
            lifecycle=lifecycle,
        )

        usage.additional_properties = d
        return usage

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
