#!/usr/bin/python
# coding=utf-8
import os

from jinja2 import Environment, FileSystemLoader
from lxml import etree

from entities.alias import Alias
from entities.entity_constructor import EntityConstructor

__author__ = "Aleksandr Shyshatsky"


class EntitiesConstructor(object):
    SCRIPTS_FOLDER = 'scripts/'
    VARIABLE_TEMPLATE = 'templates/global_variable.j2'
    VARIABLE_INIT = 'templates/__init__.j2'

    def __init__(self, base_path):
        self._base_path = base_path
        self._xml = etree.parse(
            os.path.join(base_path, self.SCRIPTS_FOLDER, 'entities.xml'))
        self._entity_constructor = EntityConstructor(base_path)
        self._entities = [None]  # entities index starts from 1

    def build_entities(self):
        """
        Build entities classes;
        """
        root, = self._xml.xpath('/root')
        for item in root:
            self._build_entities(item)

        self._build_alias()
        self._build_entities_list()
        self._build_entities_imports()

    def _build_entities(self, p_section):
        for entity in p_section:
            self._entities.append(entity.tag)
            self._get_entity_description(entity.tag)

        # touch __init__, so directory become a module
        with open('build/entities/__init__.py', 'w') as f:
            pass

        with open('build/entities/interfaces/__init__.py', 'w') as f:
            pass

    def _build_alias(self):
        path, filename = os.path.split(self.VARIABLE_TEMPLATE)
        template = Environment(loader=FileSystemLoader(path)).get_template(filename)
        alias_map = Alias(self._base_path).get_map()
        with open(os.path.join('build', '_alias.py'), 'wb') as f:
            f.write(template.render(dict(varName='g_aliasMap', value=repr(alias_map))))

    def _build_entities_list(self):
        path, filename = os.path.split(self.VARIABLE_TEMPLATE)
        template = Environment(loader=FileSystemLoader(path)).get_template(filename)
        with open(os.path.join('build', '_entities_list.py'), 'wb') as f:
            f.write(template.render(dict(varName='g_entitiesList', value=self._entities)))

    def _build_entities_imports(self):
        path, filename = os.path.split(self.VARIABLE_INIT)
        template = Environment(loader=FileSystemLoader(path)).get_template(filename)
        with open(os.path.join('build', 'entities', '__init__.py'), 'wb') as f:
            f.write(template.render(dict(entities=self._entities)))

    def _get_entity_description(self, entity_name):
        self._entity_constructor.build(entity_name)
