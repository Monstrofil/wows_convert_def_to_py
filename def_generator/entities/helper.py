#!/usr/bin/python
# coding=utf-8
from def_generator.primitive_types import STATIC_TYPES

__author__ = "Aleksandr Shyshatsky"


class VariablesLengthHelper(object):
    def __init__(self, alias_map):
        self._alias_map = alias_map

    def _get_list_size(self, type_, len_=None):
        if len_ is None:
            return 10 ** 10

        size = 0
        for _ in range(len_):
            size += self.get_variables_size([type_])
        return size

    def _get_dict_size(self, types, allow_none):
        if allow_none:
            return 10 ** 10

        size = 0
        for key, value in types:
            size += self.get_variables_size([value])
        return size

    def get_variables_size(self, arguments_list):
        """
        Get size of given arguments_list in bits.
        Returns 10**10 if size is variable.
        """
        size = 0
        for arg in arguments_list:
            if isinstance(arg, str):
                if arg in self._alias_map:
                    size += self.get_variables_size([self._alias_map[arg]])
                else:
                    size += STATIC_TYPES.get(arg, 10**10)
            elif isinstance(arg, (list, tuple)):
                if arg[0] == 'ARRAY':
                    size += self._get_list_size(*arg[1:])
                if arg[0] == 'FIXED_DICT':
                    size = self._get_dict_size(arg[1], arg[2])
        return min(10**10, size)