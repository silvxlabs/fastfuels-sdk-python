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
from enum import Enum
from typing_extensions import Self


class TreeInventorySource(str, Enum):
    """
    TreeInventorySource
    """

    """
    allowed enum values
    """
    TREEMAP = 'TreeMap'
    FILE = 'file'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TreeInventorySource from a JSON string"""
        return cls(json.loads(json_str))


