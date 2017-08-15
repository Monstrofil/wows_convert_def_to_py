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
    def from_section(cls, p_section):
        method = EntityProperty(p_section.tag)

        item, = p_section.xpath(cls.TYPE)
        if item.tag == cls.TYPE:
            type_ = item.text.strip()
            if type_ == 'ARRAY':
                elements_type, = item.xpath('of/text()')
                elements_type = elements_type.strip()
                method.argument = [[type_, elements_type]]
            elif type_ == 'FIXED_DICT':
                properties_list, = item.xpath('Properties')

                props = []
                for property in properties_list:
                    type = property.xpath('Type/text()')[0].strip()
                    tag = property.tag
                    props.append((tag, type))

                method.argument = [[type_, props]]
            else:
                method.argument = [item.text.strip()]

        try:
            default, = p_section.xpath('Default/text()')
            method.default_value = default
        except ValueError:
            pass

        return method
