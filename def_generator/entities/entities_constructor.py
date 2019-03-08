#!/usr/bin/python
# coding=utf-8
import errno
import logging
import os
import shutil

from jinja2 import Environment, FileSystemLoader
from lxml import etree

from .alias import Alias
from def_generator.entities.helper import VariablesLengthHelper
from .entity_constructor import EntityConstructor

from def_generator.entities.entity_method import EntityMethod
from def_generator.entities.entity_property import EntityProperty


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

__author__ = "Aleksandr Shyshatsky"


class EntitiesConstructor(object):
    BUILD_PATH = os.path.abspath('entity_defs_py')
    SCRIPTS_FOLDER = 'scripts/'
    TEMPLATES_PATH = os.path.join(BASE_PATH, '../templates')
    MAIN_SCRIPT = 'main.py'
    VARIABLE_TEMPLATE = 'global_variable.j2'
    VARIABLE_INIT = '__init__.j2'

    def __init__(self, base_path):
        self._base_path = base_path
        self._xml = etree.parse(
            os.path.join(base_path, self.SCRIPTS_FOLDER, 'entities.xml'))
        self._entity_constructor = None  # type: EntityConstructor
        self._entities = [None]  # entities index starts from 1

    def build_entities(self):
        """
        Build entities classes;
        """
        # create path where we will store our scripts
        logging.info("Creating directory %s for dest", self.BUILD_PATH)
        try:
            os.mkdir(self.BUILD_PATH)
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise
        # and step into it
        logging.info("Creating directory %s for dest", self.BUILD_PATH)
        os.chdir(self.BUILD_PATH)

        # alias is needed to get methods size
        argumets_helper = self._build_alias()
        # set up EntityMethod and EntityProperty
        # TODO: need some refactoring here!
        EntityMethod._argumets_helper = EntityProperty.argumets_helper = argumets_helper
        self._entity_constructor = EntityConstructor(self._base_path)

        root = self._xml.getroot()
        for item in root:
            self._build_entities(item)

        self._build_entities_list()
        self._build_entities_imports()

    def _build_entities(self, p_section):
        for entity in p_section:
            self._entities.append(entity.tag)
            self._get_entity_description(entity.tag)

        # touch __init__, so directory become a module
        with open('entities/__init__.py', 'w') as f:
            pass

        with open('entities/interfaces/__init__.py', 'w') as f:
            pass

        shutil.copy(os.path.join(self.TEMPLATES_PATH, self.MAIN_SCRIPT), self.MAIN_SCRIPT)

    def _build_alias(self):
        template = Environment(
            loader=FileSystemLoader(self.TEMPLATES_PATH)
        ).get_template(self.VARIABLE_TEMPLATE)
        alias_map = Alias(self._base_path).get_map()
        with open('_alias.py', 'w') as f:
            f.write(template.render(dict(varName='g_aliasMap', value=repr(alias_map))))
        return VariablesLengthHelper(alias_map)

    def _build_entities_list(self):
        template = Environment(
            loader=FileSystemLoader(self.TEMPLATES_PATH)
        ).get_template(self.VARIABLE_TEMPLATE)
        with open('_entities_list.py', 'w') as f:
            f.write(template.render(dict(varName='g_entitiesList', value=self._entities)))

    def _build_entities_imports(self):
        template = Environment(
            loader=FileSystemLoader(self.TEMPLATES_PATH)
        ).get_template(self.VARIABLE_INIT)
        with open(os.path.join('entities', '__init__.py'), 'w') as f:
            f.write(template.render(dict(entities=self._entities)))

    def _get_entity_description(self, entity_name):
        self._entity_constructor.build(entity_name)
