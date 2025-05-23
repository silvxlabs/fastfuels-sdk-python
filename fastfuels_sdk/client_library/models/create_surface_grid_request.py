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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from fastfuels_sdk.client_library.models.surface_grid_attribute import SurfaceGridAttribute
from fastfuels_sdk.client_library.models.surface_grid_fbfm_source import SurfaceGridFBFMSource
from fastfuels_sdk.client_library.models.surface_grid_fuel_depth_source import SurfaceGridFuelDepthSource
from fastfuels_sdk.client_library.models.surface_grid_fuel_load_source import SurfaceGridFuelLoadSource
from fastfuels_sdk.client_library.models.surface_grid_fuel_moisture_source import SurfaceGridFuelMoistureSource
from fastfuels_sdk.client_library.models.surface_grid_modification import SurfaceGridModification
from fastfuels_sdk.client_library.models.surface_grid_savr_source import SurfaceGridSAVRSource
from typing import Optional, Set
from typing_extensions import Self

class CreateSurfaceGridRequest(BaseModel):
    """
    CreateSurfaceGridRequest
    """ # noqa: E501
    attributes: Annotated[List[SurfaceGridAttribute], Field(min_length=1)] = Field(description="List of attributes to include in the surface grid")
    fuel_load: Optional[SurfaceGridFuelLoadSource] = Field(default=None, alias="fuelLoad")
    fuel_depth: Optional[SurfaceGridFuelDepthSource] = Field(default=None, alias="fuelDepth")
    fuel_moisture: Optional[SurfaceGridFuelMoistureSource] = Field(default=None, alias="fuelMoisture")
    savr: Optional[SurfaceGridSAVRSource] = Field(default=None, alias="SAVR")
    fbfm: Optional[SurfaceGridFBFMSource] = Field(default=None, alias="FBFM")
    modifications: Optional[Annotated[List[SurfaceGridModification], Field(max_length=1000)]] = Field(default=None, description="List of modifications to apply to the surface grid")
    __properties: ClassVar[List[str]] = ["attributes", "fuelLoad", "fuelDepth", "fuelMoisture", "SAVR", "FBFM", "modifications"]

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
        """Create an instance of CreateSurfaceGridRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of fuel_load
        if self.fuel_load:
            _dict['fuelLoad'] = self.fuel_load.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fuel_depth
        if self.fuel_depth:
            _dict['fuelDepth'] = self.fuel_depth.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fuel_moisture
        if self.fuel_moisture:
            _dict['fuelMoisture'] = self.fuel_moisture.to_dict()
        # override the default output from pydantic by calling `to_dict()` of savr
        if self.savr:
            _dict['SAVR'] = self.savr.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fbfm
        if self.fbfm:
            _dict['FBFM'] = self.fbfm.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in modifications (list)
        _items = []
        if self.modifications:
            for _item_modifications in self.modifications:
                if _item_modifications:
                    _items.append(_item_modifications.to_dict())
            _dict['modifications'] = _items
        # set to None if fuel_load (nullable) is None
        # and model_fields_set contains the field
        if self.fuel_load is None and "fuel_load" in self.model_fields_set:
            _dict['fuelLoad'] = None

        # set to None if fuel_depth (nullable) is None
        # and model_fields_set contains the field
        if self.fuel_depth is None and "fuel_depth" in self.model_fields_set:
            _dict['fuelDepth'] = None

        # set to None if fuel_moisture (nullable) is None
        # and model_fields_set contains the field
        if self.fuel_moisture is None and "fuel_moisture" in self.model_fields_set:
            _dict['fuelMoisture'] = None

        # set to None if savr (nullable) is None
        # and model_fields_set contains the field
        if self.savr is None and "savr" in self.model_fields_set:
            _dict['SAVR'] = None

        # set to None if fbfm (nullable) is None
        # and model_fields_set contains the field
        if self.fbfm is None and "fbfm" in self.model_fields_set:
            _dict['FBFM'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateSurfaceGridRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "attributes": obj.get("attributes"),
            "fuelLoad": SurfaceGridFuelLoadSource.from_dict(obj["fuelLoad"]) if obj.get("fuelLoad") is not None else None,
            "fuelDepth": SurfaceGridFuelDepthSource.from_dict(obj["fuelDepth"]) if obj.get("fuelDepth") is not None else None,
            "fuelMoisture": SurfaceGridFuelMoistureSource.from_dict(obj["fuelMoisture"]) if obj.get("fuelMoisture") is not None else None,
            "SAVR": SurfaceGridSAVRSource.from_dict(obj["SAVR"]) if obj.get("SAVR") is not None else None,
            "FBFM": SurfaceGridFBFMSource.from_dict(obj["FBFM"]) if obj.get("FBFM") is not None else None,
            "modifications": [SurfaceGridModification.from_dict(_item) for _item in obj["modifications"]] if obj.get("modifications") is not None else None
        })
        return _obj


