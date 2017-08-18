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

    def get_map(self):
        root, = self._xml.xpath('/root')

        for item in root:
            type_ = item.text.strip()

            self._aliases[item.tag.strip()] = type_

            if type_ == 'ARRAY':
                elements_type, = item.xpath('of/text()')
                elements_type = elements_type.strip()
                self._aliases[item.tag.strip()] = [type_, elements_type]
            elif type_ == 'FIXED_DICT':
                properties_list, = item.xpath('Properties')

                props = []
                for property in properties_list:
                    type = property.xpath('Type/text()')[0].strip()
                    tag = property.tag
                    props.append((tag, type))

                allow_none = bool(item.xpath('AllowNone'))

                self._aliases[item.tag.strip()] = [type_, props, allow_none]

        return self._aliases
