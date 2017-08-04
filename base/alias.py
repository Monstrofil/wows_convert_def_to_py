#!/usr/bin/python
# coding=utf-8
from lxml import etree, objectify

__author__ = "Aleksandr Shyshatsky"


class Alias(object):
    ALIAS_PATH = '../scripts/entity_defs/alias.xml'

    def __init__(self):
        self._xml = etree.parse(self.ALIAS_PATH, parser=etree.XMLParser(remove_comments=True))
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

                self._aliases[item.tag.strip()] = [type_, props]

        return self._aliases

g_aliasMap = Alias().get_map()
