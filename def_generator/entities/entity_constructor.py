#!/usr/bin/python
# coding=utf-8
import errno
import os

from jinja2 import Environment, FileSystemLoader
from lxml import etree

from .entity import Entity

from def_generator.entities.entity_method import EntityMethod
from def_generator.entities.entity_property import EntityProperty


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

__author__ = "Aleksandr Shyshatsky"


class EntityConstructor(object):
    """
    Constructs .py files based on given description in .def files;
    """
    TEMPLATES_PATH = os.path.join(BASE_PATH, '../templates')
    ENTITY_TEMPLATE = 'entity.j2'
    DEF_PATH = 'scripts/entity_defs'
    BUILD_DIR = 'entities'

    def __init__(self, base_path, build_subpath=''):
        self._base_path = base_path
        self._build_subpath = build_subpath

    def build(self, entity_name, interface=False):
        entity = Entity(entity_name, interface)
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
        root = etree.parse(self._get_def_path(entity.name),
                           parser=etree.XMLParser(
                                remove_comments=True,
                                remove_blank_text=True)).getroot()
        for item in root:
            # TODO: check 'CellMethods', 'BaseMethods'
            if item.tag in ('ClientMethods', ):
                entity.methods += list(self._parse_methods(item))

            if item.tag in ('Properties',):
                entity.properties += list(self._parse_properties(item))

            if item.tag in ('Implements',):
                entity.implements += list(self._parse_implements(item))

        try:
            os.makedirs(self._get_build_dir())
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise
        self._build_py(entity)

    def _parse_methods(self, p_section):
        return [EntityMethod.from_section(p_method) for p_method in p_section]

    def _parse_properties(self, p_section):
        CLIENT_FLAGS = [
            'ALL_CLIENTS', 'BASE_AND_CLIENT', 'OTHER_CLIENTS',
            'OWN_CLIENT', 'CELL_PUBLIC_AND_OWN']
        for p_property in p_section:
            flags, = p_property.xpath('Flags/text()')
            flags = flags.strip()
            if flags not in CLIENT_FLAGS:
                continue
            yield EntityProperty.from_section(p_property)

    def _parse_implements(self, p_section):
        for item in p_section:
            EntityConstructor(self._base_path, 'interfaces').build(item.text.strip(), interface=True)
        return [item.text.strip() for item in p_section]

    def _build_py(self, entity):
        template = Environment(
            loader=FileSystemLoader(self.TEMPLATES_PATH)
        ).get_template(self.ENTITY_TEMPLATE)

        with open(os.path.join(self._get_build_dir(), entity.name + '.py'), 'w') as f:
            f.write(template.render(dict(entity=entity)))
