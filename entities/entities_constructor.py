#!/usr/bin/python
# coding=utf-8
import os

from lxml import etree

from entities.entity_constructor import EntityConstructor

__author__ = "Aleksandr Shyshatsky"


class EntitiesConstructor(object):
    SCRIPTS_FOLDER = 'scripts/'

    def __init__(self, base_path):
        self._base_path = base_path
        self._xml = etree.parse(
            os.path.join(base_path, self.SCRIPTS_FOLDER, 'entities.xml'))
        self._entity_constructor = EntityConstructor(base_path)

    def build_entities(self):
        """
        Build entities classes;
        """
        root, = self._xml.xpath('/root')
        for item in root:
            self._build_entities(item)

    def _build_entities(self, p_section):
        for entity in p_section:
            self._get_entity_description(entity.tag)

    def _get_entity_description(self, entity_name):
        self._entity_constructor.build(entity_name)
