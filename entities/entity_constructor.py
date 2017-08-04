#!/usr/bin/python
# coding=utf-8
import os

from jinja2 import Environment, FileSystemLoader
from lxml import etree

from entities.entity import Entity
from entities.entity_method import EntityMethod

__author__ = "Aleksandr Shyshatsky"


class EntityConstructor(object):
    """
    Constructs .py files based on given description in .def files;
    """
    ENTITY_TEMPLATE = 'templates/entity.j2'
    DEF_PATH = 'scripts/entity_defs'
    BUILD_DIR = 'build'

    def __init__(self, base_path):
        self._base_path = base_path

    def build(self, entity_name):
        entity = Entity(entity_name)
        self._parse(entity)

    def _get_def_path(self, entity_name):
        return os.path.join(self._base_path,
                            self.DEF_PATH,
                            entity_name + '.def')

    def _parse(self, entity):
        root, = etree.parse(self._get_def_path(entity.name)).xpath('/root')

        for item in root:
            if item.tag in ('ClientMethods', 'CellMethods', 'BaseMethods'):
                entity.methods = self._parse_methods(item)

                # TODO: parse properties

        self._construct_py(entity)

    def _parse_methods(self, p_section):
        for p_method in p_section:
            method = EntityMethod.from_section(p_method)

            yield method

    def _construct_py(self, entity):
        path, filename = os.path.split(self.ENTITY_TEMPLATE)
        template = Environment(loader=FileSystemLoader(path)).get_template(filename)

        if not os.path.exists(self.BUILD_DIR):
            os.mkdir('build')
        with open(os.path.join('build', entity.name + '.py'), 'wb') as f:
            f.write(template.render(dict(entity=entity)))
