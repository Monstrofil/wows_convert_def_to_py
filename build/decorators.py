#!/usr/bin/python
# coding=utf-8
from StringIO import StringIO

from ._alias import g_aliasMap
from .primitive_types import TYPES

__author__ = "Aleksandr Shyshatsky"
__all__ = ['unpack_func_args']


def _unpack_list(stream, type_):
    size, = TYPES['UINT8'](stream)
    for _ in xrange(size):
        yield unpack_variables(stream, [type_])[0]


def _unpack_dict(stream, types):
    stream_pos = stream.pos

    # bada-boom, empty dict :)
    # check if this works with non-null dict
    if stream.read(1) == chr(0x00):
        return None
    else:
        stream.seek(stream_pos)

    kw = {}
    for key, value in types:
        kw[key] = unpack_variables(stream, [value])[0]
    return kw


def unpack_variables(stream, arguments_list):
    """
    Unpack given stream into packed_arguments;
    :param stream: 
    :return: 
    """
    if isinstance(stream, (str, unicode)):
        stream = StringIO(stream)

    unpacked = []
    for arg in arguments_list:
        if isinstance(arg, str):
            if arg in g_aliasMap:
                unpacked.extend(unpack_variables(stream, [g_aliasMap[arg]]))
            else:
                unpacked.append(TYPES[arg](stream)[0])
        elif isinstance(arg, (list, tuple)):
            if arg[0] == 'ARRAY':
                array = list(_unpack_list(stream, arg[1]))
                unpacked.append(array)
            if arg[0] == 'FIXED_DICT':
                unpacked.append(_unpack_dict(stream, arg[1]))
    return unpacked


def unpack_func_args(arguments_list):
    """
    Get's stringIO object and unpacks it into given form;
    :param list[str] arguments_list: list of arguments  
    """
    def _func_wrap(func):
        def _wrapper(self, stream):
            args = unpack_variables(stream, arguments_list)
            return func(self, *args)
        return _wrapper
    return _func_wrap
