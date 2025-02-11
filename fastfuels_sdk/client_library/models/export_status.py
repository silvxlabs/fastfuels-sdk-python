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


class ExportStatus(str, Enum):
    """
    ExportStatus
    """

    """
    allowed enum values
    """
    PENDING = 'pending'
    RUNNING = 'running'
    FAILED = 'failed'
    COMPLETED = 'completed'
    EXPIRED = 'expired'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ExportStatus from a JSON string"""
        return cls(json.loads(json_str))


