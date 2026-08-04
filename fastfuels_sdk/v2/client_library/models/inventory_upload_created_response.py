from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inventory import Inventory
    from ..models.inventory_upload_spec import InventoryUploadSpec


T = TypeVar("T", bound="InventoryUploadCreatedResponse")


@_attrs_define
class InventoryUploadCreatedResponse:
    """
    Attributes:
        inventory (Inventory): The Inventory resource.

            When status is "pending" or "running", georeference will be null.
            The backend populates it after successfully processing data,
            at which point status transitions to "completed".
        upload (InventoryUploadSpec):
    """

    inventory: Inventory
    upload: InventoryUploadSpec
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inventory = self.inventory.to_dict()

        upload = self.upload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inventory": inventory,
                "upload": upload,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.inventory import Inventory
        from ..models.inventory_upload_spec import InventoryUploadSpec

        d = dict(src_dict)
        inventory = Inventory.from_dict(d.pop("inventory"))

        upload = InventoryUploadSpec.from_dict(d.pop("upload"))

        inventory_upload_created_response = cls(
            inventory=inventory,
            upload=upload,
        )

        inventory_upload_created_response.additional_properties = d
        return inventory_upload_created_response

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
