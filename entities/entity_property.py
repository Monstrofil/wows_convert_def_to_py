#!/usr/bin/python
# coding=utf-8
__author__ = "Aleksandr Shyshatsky"


class EntityProperty(object):
    TYPE = 'Type'

    def __init__(self, p_name):
        self.name = p_name
        self.default_value = None
        self.argument = None  # type: list

    @classmethod
    def _get_dict_type(self, item):
        properties_list, = item.xpath('Properties')

        props = []
        for property in properties_list:
            pitem = property.xpath('Type')[0]
            tag = property.tag
            props.append((tag, self._get_type(pitem)))

        allow_none = bool(item.xpath('AllowNone'))

        return ['FIXED_DICT', props, allow_none]

    @classmethod
    def _get_list_type(self, item):
        elements_type, = item.xpath('of')

        size = item.xpath('size/text()')
        if size:
            return ['ARRAY', self._get_type(elements_type), int(size[0].strip())]
        return ['ARRAY', self._get_type(elements_type)]

    @classmethod
    def _get_type(self, item):
        type_ = item.text.strip()

        if type_ in ('ARRAY', 'TUPLE'):
            return self._get_list_type(item)

        elif type_ == 'FIXED_DICT':
            return self._get_dict_type(item)

        return [type_]

    @classmethod
    def from_section(cls, p_section):
        method = EntityProperty(p_section.tag)

        item, = p_section.xpath(cls.TYPE)
        if item.tag == cls.TYPE:
            method.argument = cls._get_type(item)

        try:
            default, = p_section.xpath('Default/text()')
            default = default.strip()

            try:
                default = int(default)
            except ValueError:
                pass
            else:
                try:
                    default = float(default)
                except ValueError:
                    pass

            method.default_value = default
        except ValueError:
            pass

        return method
