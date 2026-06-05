from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.resampling_method import ResamplingMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="GridAlignmentGridTarget")


@_attrs_define
class GridAlignmentGridTarget:
    """Align to an existing grid by id.

    `resolution=None` produces an exact lattice match (CRS, transform, and
    shape from the target grid). With an explicit `resolution`, the output
    keeps the target's CRS and origin but uses the new cell size; shape is
    recomputed from the target grid's bounds.

        Attributes:
            target (Literal['grid']):
            grid_id (str):
            resolution (float | None | Unset):
            method (None | ResamplingMethod | Unset):
    """

    target: Literal["grid"]
    grid_id: str
    resolution: float | None | Unset = UNSET
    method: None | ResamplingMethod | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        grid_id = self.grid_id

        resolution: float | None | Unset
        if isinstance(self.resolution, Unset):
            resolution = UNSET
        else:
            resolution = self.resolution

        method: None | str | Unset
        if isinstance(self.method, Unset):
            method = UNSET
        elif isinstance(self.method, ResamplingMethod):
            method = self.method.value
        else:
            method = self.method

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
                "grid_id": grid_id,
            }
        )
        if resolution is not UNSET:
            field_dict["resolution"] = resolution
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target = cast(Literal["grid"], d.pop("target"))
        if target != "grid":
            raise ValueError(f"target must match const 'grid', got '{target}'")

        grid_id = d.pop("grid_id")

        def _parse_resolution(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        resolution = _parse_resolution(d.pop("resolution", UNSET))

        def _parse_method(data: object) -> None | ResamplingMethod | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                method_type_0 = ResamplingMethod(data)

                return method_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ResamplingMethod | Unset, data)

        method = _parse_method(d.pop("method", UNSET))

        grid_alignment_grid_target = cls(
            target=target,
            grid_id=grid_id,
            resolution=resolution,
            method=method,
        )

        grid_alignment_grid_target.additional_properties = d
        return grid_alignment_grid_target

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
