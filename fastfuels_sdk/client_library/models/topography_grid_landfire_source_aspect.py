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
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class TopographyGridLandfireSourceAspect(BaseModel):
    """
    TopographyGridLandfireSourceAspect
    """ # noqa: E501
    source: Optional[StrictStr] = 'LANDFIRE'
    version: Optional[StrictStr] = '2020'
    interpolation_method: Optional[StrictStr] = Field(default='nearest', alias="interpolationMethod")
    __properties: ClassVar[List[str]] = ["source", "version", "interpolationMethod"]

    @field_validator('source')
    def source_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['LANDFIRE']):
            raise ValueError("must be one of enum values ('LANDFIRE')")
        return value

    @field_validator('version')
    def version_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['2020']):
            raise ValueError("must be one of enum values ('2020')")
        return value

    @field_validator('interpolation_method')
    def interpolation_method_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['nearest']):
            raise ValueError("must be one of enum values ('nearest')")
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
        """Create an instance of TopographyGridLandfireSourceAspect from a JSON string"""
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
        """Create an instance of TopographyGridLandfireSourceAspect from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "source": obj.get("source") if obj.get("source") is not None else 'LANDFIRE',
            "version": obj.get("version") if obj.get("version") is not None else '2020',
            "interpolationMethod": obj.get("interpolationMethod") if obj.get("interpolationMethod") is not None else 'nearest'
        })
        return _obj


