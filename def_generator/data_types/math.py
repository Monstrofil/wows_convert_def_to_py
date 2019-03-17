#!/usr/bin/python
# coding=utf-8
import struct
from io import BytesIO

from .base import DataType

__author__ = "Aleksandr Shyshatsky"


class _MathType(DataType):
    STRUCT_TYPE = None

    def __init__(self, header_size=1):
        assert self.STRUCT_TYPE is not None, \
            "You must define STRUCT_TYPE first"
        super().__init__(header_size=header_size)

    def _get_value_from_stream(self, stream: BytesIO, header_size: int):
        return tuple(struct.unpack(
            self.STRUCT_TYPE, stream.read(self._DATA_SIZE)))

    def _get_default_value_from_section(self, value: bytes):
        raise RuntimeError("_get_default_value_from_section for %s is not defined" % self.__class__.__name__)


class Vector2(_MathType):
    """
    VECTOR2
    — Size(bytes): 8
    Two-dimensional vector of 32-bit floats.
    Represented in Python as a tuple of two numbers (or Math.Vector2).
    """
    STRUCT_TYPE = 'ff'
    _DATA_SIZE = 8


class Vector3(_MathType):
    """
    VECTOR3
    — Size(bytes): 12
    Three-dimensional vector of 32-bit floats.
    Represented in Python as a tuple of three numbers (or Math.Vector3).
    """
    STRUCT_TYPE = 'fff'
    _DATA_SIZE = 12


class Vector4(_MathType):
    """VECTOR4 — Size(bytes): 16
    Four-dimensional vector of 32-bit floats.
    Represented in Python as a tuple of four numbers (or Math.Vector4).
    """
    STRUCT_TYPE = 'ffff'
    _DATA_SIZE = 16
