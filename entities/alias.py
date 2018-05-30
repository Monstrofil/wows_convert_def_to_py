#!/usr/bin/python
# coding=utf-8
import os

from lxml import etree

__author__ = "Aleksandr Shyshatsky"


class Alias(object):
    ALIAS_PATH = 'scripts/entity_defs/alias.xml'

    def __init__(self, base_path):
        scripts_path = os.path.join(base_path, self.ALIAS_PATH)
        self._xml = etree.parse(scripts_path, parser=etree.XMLParser(remove_comments=True))
        self._aliases = {}

    def _get_dict_type(self, item):
        properties_list, = item.xpath('Properties')

        props = []
        for property in properties_list:
            pitem = property.xpath('Type')[0]
            tag = property.tag
            props.append((tag, self._get_type(pitem)))

        allow_none = bool(item.xpath('AllowNone'))

        return ['FIXED_DICT', props, allow_none]

    def _get_list_type(self, item):
        elements_type, = item.xpath('of/text()')
        elements_type = elements_type.strip()

        size = item.xpath('size/text()')
        if size:
            return ['ARRAY', elements_type, int(size[0].strip())]
        return ['ARRAY', elements_type]

    def _get_type(self, item):
        type_ = item.text.strip()

        if type_ in ('ARRAY', 'TUPLE'):
            return self._get_list_type(item)

        elif type_ == 'FIXED_DICT':
            return self._get_dict_type(item)

        return type_

    def get_map(self):
        root, = self._xml.xpath('/root')

        for item in root:
            type_ = item.text.strip()

            self._aliases[item.tag.strip()] = self._get_type(item)

            if type_ in ('ARRAY', 'TUPLE'):
                self._aliases[item.tag.strip()] = self._get_list_type(item)
            elif type_ == 'FIXED_DICT':
                self._aliases[item.tag.strip()] = self._get_dict_type(item)

        return self._aliases
