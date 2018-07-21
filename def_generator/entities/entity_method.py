#!/usr/bin/python
# coding=utf-8

__author__ = "Aleksandr Shyshatsky"


class EntityMethod(object):
    ARG = 'Arg'

    # statspublisher interface has the other def structure
    # <receivePublicIntStat>
    #   <Args>
    #     <stat_id> STRING </stat_id>
    #     <value> INT32 </value>
    #     <add> BOOL </add>
    #   </Args>
    # </receivePublicIntStat>
    ARGS = 'Args'

    _argumets_helper = None  # FIXME: refactor this stuff and remove static vars

    def __init__(self, p_name):
        self.name = p_name
        self.arguments = []
        self.header_size = 1

    @property
    def size(self):
        return self._argumets_helper\
                   .get_variables_size(self.arguments) + self.header_size

    @classmethod
    def _get_dict_type(cls, item):
        properties_list, = item.xpath('Properties')

        props = []
        for property in properties_list:
            pitem = property.xpath('Type')[0]
            tag = property.tag
            props.append((tag, cls._get_type(pitem)))

        allow_none = bool(item.xpath('AllowNone'))

        return ['FIXED_DICT', props, allow_none]

    @classmethod
    def _get_list_type(cls, item):
        elements_type, = item.xpath('of')

        size = item.xpath('size/text()')
        if size:
            return ['ARRAY', cls._get_type(elements_type), int(size[0].strip())]
        return ['ARRAY', cls._get_type(elements_type)]

    @classmethod
    def _get_type(cls, item):
        type_ = item.text.strip()
        if type_ in ('ARRAY', 'TUPLE'):
            return cls._get_list_type(item)
        elif type_ == 'FIXED_DICT':
            return cls._get_dict_type(item)
        return type_

    @classmethod
    def from_section(cls, p_section):
        method = EntityMethod(p_section.tag)

        for item in p_section:
            if item.tag == cls.ARG:
                method.arguments.append(cls._get_type(item))
            if item.tag == cls.ARGS:
                for arg in item:
                    method.arguments.append(cls._get_type(arg))
            if item.tag == 'VariableLengthHeaderSize':
                # TODO: use this tag during arguments parsing
                method.header_size = int(item.text.strip())
        return method
