#!/usr/bin/python
# coding=utf-8
__author__ = "Aleksandr Shyshatsky"


class EntityMethod(object):
    ARG = 'Arg'

    def __init__(self, p_name):
        self.name = p_name
        self.arguments = []

    @classmethod
    def from_section(cls, p_section):
        method = EntityMethod(p_section.tag)

        for item in p_section:
            if item.tag == cls.ARG:
                type_ = item.text.strip()
                if type_ == 'ARRAY':
                    elements_type, = item.xpath('of/text()')
                    elements_type = elements_type.strip()
                    method.arguments.append([type_, elements_type])
                elif type_ == 'FIXED_DICT':
                    properties_list, = item.xpath('Properties')

                    props = []
                    for property in properties_list:
                        type = property.xpath('Type/text()')[0].strip()
                        tag = property.tag
                        props.append((tag, type))

                    method.arguments.append([type_, props])
                else:
                    method.arguments.append(item.text.strip())
        return method