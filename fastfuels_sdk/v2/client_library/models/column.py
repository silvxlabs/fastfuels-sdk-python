from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.column_type import ColumnType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.categorical_column_summary import CategoricalColumnSummary
    from ..models.continuous_column_summary import ContinuousColumnSummary


T = TypeVar("T", bound="Column")


@_attrs_define
class Column:
    """A single column in an inventory.

    Attributes:
        key (str): Column name (e.g., 'dbh', 'fia_species_code')
        type_ (ColumnType): Type of column data.
        unit (None | str | Unset):
        summary (CategoricalColumnSummary | ContinuousColumnSummary | None | Unset):
    """

    key: str
    type_: ColumnType
    unit: None | str | Unset = UNSET
    summary: CategoricalColumnSummary | ContinuousColumnSummary | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.categorical_column_summary import CategoricalColumnSummary
        from ..models.continuous_column_summary import ContinuousColumnSummary

        key = self.key

        type_ = self.type_.value

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        else:
            unit = self.unit

        summary: dict[str, Any] | None | Unset
        if isinstance(self.summary, Unset):
            summary = UNSET
        elif isinstance(self.summary, ContinuousColumnSummary) or isinstance(
            self.summary, CategoricalColumnSummary
        ):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "type": type_,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.categorical_column_summary import CategoricalColumnSummary
        from ..models.continuous_column_summary import ContinuousColumnSummary

        d = dict(src_dict)
        key = d.pop("key")

        type_ = ColumnType(d.pop("type"))

        def _parse_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        def _parse_summary(
            data: object,
        ) -> CategoricalColumnSummary | ContinuousColumnSummary | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0_type_0 = ContinuousColumnSummary.from_dict(data)

                return summary_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0_type_1 = CategoricalColumnSummary.from_dict(data)

                return summary_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(
                CategoricalColumnSummary | ContinuousColumnSummary | None | Unset, data
            )

        summary = _parse_summary(d.pop("summary", UNSET))

        column = cls(
            key=key,
            type_=type_,
            unit=unit,
            summary=summary,
        )

        column.additional_properties = d
        return column

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
