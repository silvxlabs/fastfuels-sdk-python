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
from fastfuels_sdk.client_library.models.surface_grid_modification_fbfm_action import SurfaceGridModificationFBFMAction
from fastfuels_sdk.client_library.models.surface_grid_modification_fuel_height_action import SurfaceGridModificationFuelHeightAction
from fastfuels_sdk.client_library.models.surface_grid_modification_fuel_load_action import SurfaceGridModificationFuelLoadAction
from fastfuels_sdk.client_library.models.surface_grid_modification_fuel_moisture_action import SurfaceGridModificationFuelMoistureAction
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

SURFACEGRIDMODIFICATIONACTION_ONE_OF_SCHEMAS = ["SurfaceGridModificationFBFMAction", "SurfaceGridModificationFuelHeightAction", "SurfaceGridModificationFuelLoadAction", "SurfaceGridModificationFuelMoistureAction"]

class SurfaceGridModificationAction(BaseModel):
    """
    The actions for the surface grid modification.
    """
    # data type: SurfaceGridModificationFBFMAction
    oneof_schema_1_validator: Optional[SurfaceGridModificationFBFMAction] = None
    # data type: SurfaceGridModificationFuelLoadAction
    oneof_schema_2_validator: Optional[SurfaceGridModificationFuelLoadAction] = None
    # data type: SurfaceGridModificationFuelHeightAction
    oneof_schema_3_validator: Optional[SurfaceGridModificationFuelHeightAction] = None
    # data type: SurfaceGridModificationFuelMoistureAction
    oneof_schema_4_validator: Optional[SurfaceGridModificationFuelMoistureAction] = None
    actual_instance: Optional[Union[SurfaceGridModificationFBFMAction, SurfaceGridModificationFuelHeightAction, SurfaceGridModificationFuelLoadAction, SurfaceGridModificationFuelMoistureAction]] = None
    one_of_schemas: Set[str] = { "SurfaceGridModificationFBFMAction", "SurfaceGridModificationFuelHeightAction", "SurfaceGridModificationFuelLoadAction", "SurfaceGridModificationFuelMoistureAction" }

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
        instance = SurfaceGridModificationAction.model_construct()
        error_messages = []
        match = 0
        # validate data type: SurfaceGridModificationFBFMAction
        if not isinstance(v, SurfaceGridModificationFBFMAction):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFBFMAction`")
        else:
            match += 1
        # validate data type: SurfaceGridModificationFuelLoadAction
        if not isinstance(v, SurfaceGridModificationFuelLoadAction):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFuelLoadAction`")
        else:
            match += 1
        # validate data type: SurfaceGridModificationFuelHeightAction
        if not isinstance(v, SurfaceGridModificationFuelHeightAction):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFuelHeightAction`")
        else:
            match += 1
        # validate data type: SurfaceGridModificationFuelMoistureAction
        if not isinstance(v, SurfaceGridModificationFuelMoistureAction):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SurfaceGridModificationFuelMoistureAction`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in SurfaceGridModificationAction with oneOf schemas: SurfaceGridModificationFBFMAction, SurfaceGridModificationFuelHeightAction, SurfaceGridModificationFuelLoadAction, SurfaceGridModificationFuelMoistureAction. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in SurfaceGridModificationAction with oneOf schemas: SurfaceGridModificationFBFMAction, SurfaceGridModificationFuelHeightAction, SurfaceGridModificationFuelLoadAction, SurfaceGridModificationFuelMoistureAction. Details: " + ", ".join(error_messages))
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

        # deserialize data into SurfaceGridModificationFBFMAction
        try:
            instance.actual_instance = SurfaceGridModificationFBFMAction.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SurfaceGridModificationFuelLoadAction
        try:
            instance.actual_instance = SurfaceGridModificationFuelLoadAction.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SurfaceGridModificationFuelHeightAction
        try:
            instance.actual_instance = SurfaceGridModificationFuelHeightAction.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into SurfaceGridModificationFuelMoistureAction
        try:
            instance.actual_instance = SurfaceGridModificationFuelMoistureAction.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into SurfaceGridModificationAction with oneOf schemas: SurfaceGridModificationFBFMAction, SurfaceGridModificationFuelHeightAction, SurfaceGridModificationFuelLoadAction, SurfaceGridModificationFuelMoistureAction. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into SurfaceGridModificationAction with oneOf schemas: SurfaceGridModificationFBFMAction, SurfaceGridModificationFuelHeightAction, SurfaceGridModificationFuelLoadAction, SurfaceGridModificationFuelMoistureAction. Details: " + ", ".join(error_messages))
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], SurfaceGridModificationFBFMAction, SurfaceGridModificationFuelHeightAction, SurfaceGridModificationFuelLoadAction, SurfaceGridModificationFuelMoistureAction]]:
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


