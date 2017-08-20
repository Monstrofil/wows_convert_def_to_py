#!/usr/bin/python
# coding=utf-8
import os

from jinja2 import Environment, FileSystemLoader
from lxml import etree

from entities.entity import Entity
from entities.entity_method import EntityMethod
from entities.entity_property import EntityProperty

__author__ = "Aleksandr Shyshatsky"


class EntityConstructor(object):
    """
    Constructs .py files based on given description in .def files;
    """
    ENTITY_TEMPLATE = 'templates/entity.j2'
    DEF_PATH = 'scripts/entity_defs'
    BUILD_DIR = 'build/entities'

    def __init__(self, base_path, build_subpath=''):
        self._base_path = base_path
        self._build_subpath = build_subpath

    def build(self, entity_name):
        entity = Entity(entity_name)
        self._parse(entity)

    def _get_def_path(self, entity_name):
        return os.path.join(self._base_path,
                            self.DEF_PATH,
                            self._build_subpath,
                            entity_name + '.def')

    def _get_build_dir(self):
        return os.path.join(self.BUILD_DIR,
                            self._build_subpath)

    def _parse(self, entity):
        root, = etree.parse(self._get_def_path(entity.name), parser=etree.XMLParser(remove_comments=True)).xpath('/root')

        for item in root:
            if item.tag in ('ClientMethods', 'CellMethods', 'BaseMethods'):
                entity.methods += list(self._parse_methods(item))

            if item.tag in ('Properties',):
                entity.properties += list(self._parse_properties(item))

            if item.tag in ('Implements',):
                entity.implements += list(self._parse_implements(item))

        if not os.path.exists(self._get_build_dir()):
            os.mkdir(self._get_build_dir())
        self._build_py(entity)

    def _parse_methods(self, p_section):
        return [EntityMethod.from_section(p_method) for p_method in p_section]

    def _parse_properties(self, p_section):
        return [EntityProperty.from_section(p_method) for p_method in p_section]

    def _parse_implements(self, p_section):
        for item in p_section:
            EntityConstructor(self._base_path, 'interfaces').build(item.text.strip())
        return [item.text.strip() for item in p_section]

    def _build_py(self, entity):
        path, filename = os.path.split(self.ENTITY_TEMPLATE)
        template = Environment(loader=FileSystemLoader(path)).get_template(filename)

        with open(os.path.join(self._get_build_dir(), entity.name + '.py'), 'wb') as f:
            f.write(template.render(dict(entity=entity)))
