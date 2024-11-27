# coding: utf-8

"""
    FastFuels API

    A JSON API for creating, editing, and retrieving 3D fuels data for next generation fire behavior models.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from fastfuels_sdk.client_library.models.feature_type import FeatureType
from typing import Optional, Set
from typing_extensions import Self

class UniformFBFM40SizeClassValue(BaseModel):
    """
    UniformFBFM40SizeClassValue
    """ # noqa: E501
    feature_masks: Optional[List[FeatureType]] = Field(default=None, description="List of feature masks to apply to the surface grid attribute", alias="featureMasks")
    source: Optional[StrictStr] = 'uniformByFBFM40SizeClass'
    one_hour: Union[Annotated[float, Field(strict=True, ge=0.0)], Annotated[int, Field(strict=True, ge=0)]] = Field(alias="oneHour")
    ten_hour: Union[Annotated[float, Field(strict=True, ge=0.0)], Annotated[int, Field(strict=True, ge=0)]] = Field(alias="tenHour")
    hundred_hour: Union[Annotated[float, Field(strict=True, ge=0.0)], Annotated[int, Field(strict=True, ge=0)]] = Field(alias="hundredHour")
    live_herbaceous: Union[Annotated[float, Field(strict=True, ge=0.0)], Annotated[int, Field(strict=True, ge=0)]] = Field(alias="liveHerbaceous")
    live_woody: Union[Annotated[float, Field(strict=True, ge=0.0)], Annotated[int, Field(strict=True, ge=0)]] = Field(alias="liveWoody")
    __properties: ClassVar[List[str]] = ["featureMasks", "source", "oneHour", "tenHour", "hundredHour", "liveHerbaceous", "liveWoody"]

    @field_validator('source')
    def source_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['uniformByFBFM40SizeClass']):
            raise ValueError("must be one of enum values ('uniformByFBFM40SizeClass')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UniformFBFM40SizeClassValue from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UniformFBFM40SizeClassValue from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "featureMasks": obj.get("featureMasks"),
            "source": obj.get("source") if obj.get("source") is not None else 'uniformByFBFM40SizeClass',
            "oneHour": obj.get("oneHour"),
            "tenHour": obj.get("tenHour"),
            "hundredHour": obj.get("hundredHour"),
            "liveHerbaceous": obj.get("liveHerbaceous"),
            "liveWoody": obj.get("liveWoody")
        })
        return _obj


