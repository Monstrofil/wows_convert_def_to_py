#!/usr/bin/python
# coding=utf-8
from StringIO import StringIO

try:
    from build._alias import g_aliasMap
except ImportError:
    from _alias import g_aliasMap
from primitive_types import TYPES
from nested_types import PyFixedDict, PyFixedList

__author__ = "Aleksandr Shyshatsky"
__all__ = ['unpack_func_args']


def _unpack_list(stream, type_, size=None):
    if size is None:
        size, = TYPES['UINT8'](stream)

    array = PyFixedList(type_)
    for _ in xrange(size):
        array.append(unpack_variables(stream, [type_])[0])
    return array


def _unpack_dict(stream, types, allow_none):
    stream_pos = stream.pos

    # bada-boom, empty dict :)
    # check if this works with non-null dict
    if allow_none:
        flag = stream.read(1)
        # stream.seek(stream_pos)
        if flag == chr(0x00):
            return None
        elif flag == chr(0x01):
            # not empty dict
            pass
        else:
            stream.seek(stream_pos)

    kw = PyFixedDict(types)
    for key, value in types:
        kw[key] = unpack_variables(stream, [value])[0]
    return kw


def unpack_variables(stream, arguments_list, with_tell=False):
    """
    Unpack given stream into packed_arguments;
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
                array = _unpack_list(stream, *arg[1:])
                unpacked.append(array)
            if arg[0] == 'FIXED_DICT':
                unpacked.append(_unpack_dict(stream, arg[1], arg[2]))
    if with_tell:
        return unpacked, stream.tell()
    return unpacked


def unpack_func_args(arguments_list):
    """
    Get's stringIO object and unpacks it into given form;
    :param list[str] arguments_list: list of arguments  
    """
    def _func_wrap(func):
        def _wrapper(self, stream):
            args, tell = unpack_variables(stream, arguments_list, with_tell=True)
            assert tell == len(stream), "Something wrong with unpack method"
            return func(self, *args)
        return _wrapper
    return _func_wrap
