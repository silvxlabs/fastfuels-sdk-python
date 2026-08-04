from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Quotas")


@_attrs_define
class Quotas:
    """Usage limits for an owner. Field defaults are the standard tier.

    Attributes:
        max_active_grids (int | Unset):  Default: 25.
        max_active_exports (int | Unset):  Default: 10.
        max_active_inventories (int | Unset):  Default: 10.
        max_active_features (int | Unset):  Default: 10.
        max_active_pointclouds (int | Unset):  Default: 5.
        max_domains (int | Unset):  Default: 50.
        max_grids (int | Unset):  Default: 1000.
        max_exports (int | Unset):  Default: 500.
        max_inventories (int | Unset):  Default: 500.
        max_features (int | Unset):  Default: 500.
        max_pointclouds (int | Unset):  Default: 50.
        max_api_keys (int | Unset):  Default: 50.
        max_applications (int | Unset):  Default: 5.
        max_grid_storage_bytes (int | Unset):  Default: 53687091200.
        max_export_storage_bytes (int | Unset):  Default: 26843545600.
        max_inventory_storage_bytes (int | Unset):  Default: 10737418240.
        max_feature_storage_bytes (int | Unset):  Default: 1073741824.
        max_pointcloud_storage_bytes (int | Unset):  Default: 53687091200.
        max_weekly_grid_dispatches (int | Unset): Grid worker jobs allowed per ISO week (Monday 00:00 UTC reset):
            creates, modifications, duplicates, and uploads all count. Deleting grids does not refund spent budget. Default:
            500.
        max_weekly_export_dispatches (int | Unset): Export worker jobs allowed per ISO week (Monday 00:00 UTC reset).
            Deleting exports does not refund spent budget. Default: 250.
        max_weekly_inventory_dispatches (int | Unset): Inventory worker jobs allowed per ISO week (Monday 00:00 UTC
            reset): creates, modifications, treatments, duplicates, and uploads all count. Deleting inventories does not
            refund spent budget. Default: 250.
        max_weekly_feature_dispatches (int | Unset): Feature worker jobs allowed per ISO week (Monday 00:00 UTC reset).
            Synchronous layerset creates are exempt. Deleting features does not refund spent budget. Default: 250.
        max_weekly_pointcloud_dispatches (int | Unset): Point cloud worker jobs allowed per ISO week (Monday 00:00 UTC
            reset): each upload counts. Deleting point clouds does not refund spent budget. Default: 50.
        resource_ttl_days (int | None | Unset):  Default: 180.
        failed_resource_ttl_days (int | None | Unset):  Default: 14.
    """

    max_active_grids: int | Unset = 25
    max_active_exports: int | Unset = 10
    max_active_inventories: int | Unset = 10
    max_active_features: int | Unset = 10
    max_active_pointclouds: int | Unset = 5
    max_domains: int | Unset = 50
    max_grids: int | Unset = 1000
    max_exports: int | Unset = 500
    max_inventories: int | Unset = 500
    max_features: int | Unset = 500
    max_pointclouds: int | Unset = 50
    max_api_keys: int | Unset = 50
    max_applications: int | Unset = 5
    max_grid_storage_bytes: int | Unset = 53687091200
    max_export_storage_bytes: int | Unset = 26843545600
    max_inventory_storage_bytes: int | Unset = 10737418240
    max_feature_storage_bytes: int | Unset = 1073741824
    max_pointcloud_storage_bytes: int | Unset = 53687091200
    max_weekly_grid_dispatches: int | Unset = 500
    max_weekly_export_dispatches: int | Unset = 250
    max_weekly_inventory_dispatches: int | Unset = 250
    max_weekly_feature_dispatches: int | Unset = 250
    max_weekly_pointcloud_dispatches: int | Unset = 50
    resource_ttl_days: int | None | Unset = 180
    failed_resource_ttl_days: int | None | Unset = 14
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_active_grids = self.max_active_grids

        max_active_exports = self.max_active_exports

        max_active_inventories = self.max_active_inventories

        max_active_features = self.max_active_features

        max_active_pointclouds = self.max_active_pointclouds

        max_domains = self.max_domains

        max_grids = self.max_grids

        max_exports = self.max_exports

        max_inventories = self.max_inventories

        max_features = self.max_features

        max_pointclouds = self.max_pointclouds

        max_api_keys = self.max_api_keys

        max_applications = self.max_applications

        max_grid_storage_bytes = self.max_grid_storage_bytes

        max_export_storage_bytes = self.max_export_storage_bytes

        max_inventory_storage_bytes = self.max_inventory_storage_bytes

        max_feature_storage_bytes = self.max_feature_storage_bytes

        max_pointcloud_storage_bytes = self.max_pointcloud_storage_bytes

        max_weekly_grid_dispatches = self.max_weekly_grid_dispatches

        max_weekly_export_dispatches = self.max_weekly_export_dispatches

        max_weekly_inventory_dispatches = self.max_weekly_inventory_dispatches

        max_weekly_feature_dispatches = self.max_weekly_feature_dispatches

        max_weekly_pointcloud_dispatches = self.max_weekly_pointcloud_dispatches

        resource_ttl_days: int | None | Unset
        if isinstance(self.resource_ttl_days, Unset):
            resource_ttl_days = UNSET
        else:
            resource_ttl_days = self.resource_ttl_days

        failed_resource_ttl_days: int | None | Unset
        if isinstance(self.failed_resource_ttl_days, Unset):
            failed_resource_ttl_days = UNSET
        else:
            failed_resource_ttl_days = self.failed_resource_ttl_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if max_active_grids is not UNSET:
            field_dict["max_active_grids"] = max_active_grids
        if max_active_exports is not UNSET:
            field_dict["max_active_exports"] = max_active_exports
        if max_active_inventories is not UNSET:
            field_dict["max_active_inventories"] = max_active_inventories
        if max_active_features is not UNSET:
            field_dict["max_active_features"] = max_active_features
        if max_active_pointclouds is not UNSET:
            field_dict["max_active_pointclouds"] = max_active_pointclouds
        if max_domains is not UNSET:
            field_dict["max_domains"] = max_domains
        if max_grids is not UNSET:
            field_dict["max_grids"] = max_grids
        if max_exports is not UNSET:
            field_dict["max_exports"] = max_exports
        if max_inventories is not UNSET:
            field_dict["max_inventories"] = max_inventories
        if max_features is not UNSET:
            field_dict["max_features"] = max_features
        if max_pointclouds is not UNSET:
            field_dict["max_pointclouds"] = max_pointclouds
        if max_api_keys is not UNSET:
            field_dict["max_api_keys"] = max_api_keys
        if max_applications is not UNSET:
            field_dict["max_applications"] = max_applications
        if max_grid_storage_bytes is not UNSET:
            field_dict["max_grid_storage_bytes"] = max_grid_storage_bytes
        if max_export_storage_bytes is not UNSET:
            field_dict["max_export_storage_bytes"] = max_export_storage_bytes
        if max_inventory_storage_bytes is not UNSET:
            field_dict["max_inventory_storage_bytes"] = max_inventory_storage_bytes
        if max_feature_storage_bytes is not UNSET:
            field_dict["max_feature_storage_bytes"] = max_feature_storage_bytes
        if max_pointcloud_storage_bytes is not UNSET:
            field_dict["max_pointcloud_storage_bytes"] = max_pointcloud_storage_bytes
        if max_weekly_grid_dispatches is not UNSET:
            field_dict["max_weekly_grid_dispatches"] = max_weekly_grid_dispatches
        if max_weekly_export_dispatches is not UNSET:
            field_dict["max_weekly_export_dispatches"] = max_weekly_export_dispatches
        if max_weekly_inventory_dispatches is not UNSET:
            field_dict["max_weekly_inventory_dispatches"] = (
                max_weekly_inventory_dispatches
            )
        if max_weekly_feature_dispatches is not UNSET:
            field_dict["max_weekly_feature_dispatches"] = max_weekly_feature_dispatches
        if max_weekly_pointcloud_dispatches is not UNSET:
            field_dict["max_weekly_pointcloud_dispatches"] = (
                max_weekly_pointcloud_dispatches
            )
        if resource_ttl_days is not UNSET:
            field_dict["resource_ttl_days"] = resource_ttl_days
        if failed_resource_ttl_days is not UNSET:
            field_dict["failed_resource_ttl_days"] = failed_resource_ttl_days

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_active_grids = d.pop("max_active_grids", UNSET)

        max_active_exports = d.pop("max_active_exports", UNSET)

        max_active_inventories = d.pop("max_active_inventories", UNSET)

        max_active_features = d.pop("max_active_features", UNSET)

        max_active_pointclouds = d.pop("max_active_pointclouds", UNSET)

        max_domains = d.pop("max_domains", UNSET)

        max_grids = d.pop("max_grids", UNSET)

        max_exports = d.pop("max_exports", UNSET)

        max_inventories = d.pop("max_inventories", UNSET)

        max_features = d.pop("max_features", UNSET)

        max_pointclouds = d.pop("max_pointclouds", UNSET)

        max_api_keys = d.pop("max_api_keys", UNSET)

        max_applications = d.pop("max_applications", UNSET)

        max_grid_storage_bytes = d.pop("max_grid_storage_bytes", UNSET)

        max_export_storage_bytes = d.pop("max_export_storage_bytes", UNSET)

        max_inventory_storage_bytes = d.pop("max_inventory_storage_bytes", UNSET)

        max_feature_storage_bytes = d.pop("max_feature_storage_bytes", UNSET)

        max_pointcloud_storage_bytes = d.pop("max_pointcloud_storage_bytes", UNSET)

        max_weekly_grid_dispatches = d.pop("max_weekly_grid_dispatches", UNSET)

        max_weekly_export_dispatches = d.pop("max_weekly_export_dispatches", UNSET)

        max_weekly_inventory_dispatches = d.pop(
            "max_weekly_inventory_dispatches", UNSET
        )

        max_weekly_feature_dispatches = d.pop("max_weekly_feature_dispatches", UNSET)

        max_weekly_pointcloud_dispatches = d.pop(
            "max_weekly_pointcloud_dispatches", UNSET
        )

        def _parse_resource_ttl_days(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        resource_ttl_days = _parse_resource_ttl_days(d.pop("resource_ttl_days", UNSET))

        def _parse_failed_resource_ttl_days(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        failed_resource_ttl_days = _parse_failed_resource_ttl_days(
            d.pop("failed_resource_ttl_days", UNSET)
        )

        quotas = cls(
            max_active_grids=max_active_grids,
            max_active_exports=max_active_exports,
            max_active_inventories=max_active_inventories,
            max_active_features=max_active_features,
            max_active_pointclouds=max_active_pointclouds,
            max_domains=max_domains,
            max_grids=max_grids,
            max_exports=max_exports,
            max_inventories=max_inventories,
            max_features=max_features,
            max_pointclouds=max_pointclouds,
            max_api_keys=max_api_keys,
            max_applications=max_applications,
            max_grid_storage_bytes=max_grid_storage_bytes,
            max_export_storage_bytes=max_export_storage_bytes,
            max_inventory_storage_bytes=max_inventory_storage_bytes,
            max_feature_storage_bytes=max_feature_storage_bytes,
            max_pointcloud_storage_bytes=max_pointcloud_storage_bytes,
            max_weekly_grid_dispatches=max_weekly_grid_dispatches,
            max_weekly_export_dispatches=max_weekly_export_dispatches,
            max_weekly_inventory_dispatches=max_weekly_inventory_dispatches,
            max_weekly_feature_dispatches=max_weekly_feature_dispatches,
            max_weekly_pointcloud_dispatches=max_weekly_pointcloud_dispatches,
            resource_ttl_days=resource_ttl_days,
            failed_resource_ttl_days=failed_resource_ttl_days,
        )

        quotas.additional_properties = d
        return quotas

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
