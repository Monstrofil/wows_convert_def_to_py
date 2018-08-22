#!/usr/bin/python
# coding=utf-8
__author__ = "Aleksandr Shyshatsky"


class PyFixedDict(dict):
    """
    Emulate BigWorld type PyFixedDict
    """
    def __init__(self, attributes, *args, **kwargs):
        self._attributes = attributes
        super(PyFixedDict, self).__init__(*args, **kwargs)

    def get_field_name_for_index(self, index):
        return self._attributes[index][0]

    def get_field_type_for_index(self, index):
        return self._attributes[index][1]


# TODO: hardcoded list len
class PyFixedList(list):
    """
    Emulate BigWorld type PyFixedList
    """
    def __init__(self, element_type, *args, **kwargs):
        super(PyFixedList, self).__init__(*args, **kwargs)
        if element_type is None:
            raise NotImplementedError("element_type must be not None")
        self._element_type = element_type

    def get_field_name_for_index(self, index):
        return index

    def get_element_type(self):
        return self._element_type
