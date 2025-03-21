# coding: utf-8

"""
    FastFuels API

    A JSON API for creating, editing, and retrieving 3D fuels data for next generation fire behavior models.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from fastfuels_sdk.client_library.models.surface_grid_modification_fbfm_condition import SurfaceGridModificationFBFMCondition
from fastfuels_sdk.client_library.models.surface_grid_modification_fuel_height_condition import SurfaceGridModificationFuelHeightCondition
from fastfuels_sdk.client_library.models.surface_grid_modification_fuel_load_condition import SurfaceGridModificationFuelLoadCondition
from fastfuels_sdk.client_library.models.surface_grid_modification_fuel_moisture_condition import SurfaceGridModificationFuelMoistureCondition
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

SURFACEGRIDMODIFICATIONCONDITION_ONE_OF_SCHEMAS = ["SurfaceGridModificationFBFMCondition", "SurfaceGridModificationFuelHeightCondition", "SurfaceGridModificationFuelLoadCondition", "SurfaceGridModificationFuelMoistureCondition"]

class SurfaceGridModificationCondition(BaseModel):
    """
    The conditions for the surface grid modification.
    """
    # data type: SurfaceGridModificationFBFMCondition
    oneof_schema_1_validator: Optional[SurfaceGridModificationFBFMCondition] = None
    # data type: SurfaceGridModificationFuelLoadCondition
    oneof_schema_2_validator: Optional[SurfaceGridModificationFuelLoadCondition] = None
    # data type: SurfaceGridModificationFuelHeightCondition
    oneof_schema_3_validator: Optional[SurfaceGridModificationFuelHeightCondition] = None
    # data type: SurfaceGridModificationFuelMoistureCondition
    oneof_schema_4_validator: Optional[SurfaceGridModificationFuelMoistureCondition] = None
    actual_instance: Optional[Union[SurfaceGridModificationFBFMCondition, SurfaceGridModificationFuelHeightCondition, SurfaceGridModificationFuelLoadCondition, SurfaceGridModificationFuelMoistureCondition]] = None
    one_of_schemas: Set[str] = { "SurfaceGridModificationFBFMCondition", "SurfaceGridModificationFuelHeightCondition", "SurfaceGridModificationFuelLoadCondition", "SurfaceGridModificationFuelMoistureCondition" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = SurfaceGridModificationCondition.model_construct()
        error_messages = []
        match = 0
        # validate data type: SurfaceGridModificationFBFMCondition
        if not isinstance(v, SurfaceGridModificationFBFMCondition):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFBFMCondition`")
        else:
            match += 1
        # validate data type: SurfaceGridModificationFuelLoadCondition
        if not isinstance(v, SurfaceGridModificationFuelLoadCondition):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFuelLoadCondition`")
        else:
            match += 1
        # validate data type: SurfaceGridModificationFuelHeightCondition
        if not isinstance(v, SurfaceGridModificationFuelHeightCondition):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFuelHeightCondition`")
        else:
            match += 1
        # validate data type: SurfaceGridModificationFuelMoistureCondition
        if not isinstance(v, SurfaceGridModificationFuelMoistureCondition):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFuelMoistureCondition`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in SurfaceGridModificationCondition with oneOf schemas: SurfaceGridModificationFBFMCondition, SurfaceGridModificationFuelHeightCondition, SurfaceGridModificationFuelLoadCondition, SurfaceGridModificationFuelMoistureCondition. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in SurfaceGridModificationCondition with oneOf schemas: SurfaceGridModificationFBFMCondition, SurfaceGridModificationFuelHeightCondition, SurfaceGridModificationFuelLoadCondition, SurfaceGridModificationFuelMoistureCondition. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into SurfaceGridModificationFBFMCondition
        try:
            instance.actual_instance = SurfaceGridModificationFBFMCondition.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SurfaceGridModificationFuelLoadCondition
        try:
            instance.actual_instance = SurfaceGridModificationFuelLoadCondition.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SurfaceGridModificationFuelHeightCondition
        try:
            instance.actual_instance = SurfaceGridModificationFuelHeightCondition.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SurfaceGridModificationFuelMoistureCondition
        try:
            instance.actual_instance = SurfaceGridModificationFuelMoistureCondition.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into SurfaceGridModificationCondition with oneOf schemas: SurfaceGridModificationFBFMCondition, SurfaceGridModificationFuelHeightCondition, SurfaceGridModificationFuelLoadCondition, SurfaceGridModificationFuelMoistureCondition. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into SurfaceGridModificationCondition with oneOf schemas: SurfaceGridModificationFBFMCondition, SurfaceGridModificationFuelHeightCondition, SurfaceGridModificationFuelLoadCondition, SurfaceGridModificationFuelMoistureCondition. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], SurfaceGridModificationFBFMCondition, SurfaceGridModificationFuelHeightCondition, SurfaceGridModificationFuelLoadCondition, SurfaceGridModificationFuelMoistureCondition]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


