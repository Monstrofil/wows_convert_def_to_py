#!/usr/bin/python
# coding=utf-8
import os
from io import BytesIO
from typing import List, Dict, Optional

from lxml import etree

from def_generator.constants import ENTITIES_DEFS_PATH, INFINITY, EntityFlags
from def_generator.data_types import DataType, Alias

DEFAULT_HEADER_SIZE = 1

__author__ = "Aleksandr Shyshatsky"


class MethodArgument:
    def __init__(self, type_: DataType, name=None):
        self.name = name
        self.type = type_

    def __repr__(self):
        if self.name:
            return '%s: %s' % (self.name, self.type)
        return 'unknown: %s' % self.type


class EntityMethod:

    def __init__(self, name, arguments: List[MethodArgument], header_size: int = DEFAULT_HEADER_SIZE):
        self._name = name or None
        self._arguments = arguments
        self._variable_header_size = header_size

    def get_name(self):
        return self._name

    def get_size_in_bytes(self):
        size = sum(i.type.get_size_in_bytes() for i in self._arguments)
        if size >= INFINITY:
            return INFINITY + self._variable_header_size
        return size + self._variable_header_size

    def _get_header_size_from_section(self, section: etree.ElementBase):
        """
        E.g.
        <onEnterPreBattle>
            <Arg>BLOB</Arg>
            <VariableLengthHeaderSize>
                <WarnLevel>none</WarnLevel>
            </VariableLengthHeaderSize>
        </onEnterPreBattle>
        """
        if section.find('VariableLengthHeaderSize'):
            return int(section.find('VariableLengthHeaderSize').text.strip())
        return None

    @classmethod
    def from_section(cls, section: etree.ElementBase, alias):
        args = []
        if section.find('Args') is not None:
            for item in section.find('Args'):
                args.append(MethodArgument(
                    name=item.tag, type_=alias.get_data_type_from_section(item)))
        else:
            for item in section.findall('Arg'):
                args.append(MethodArgument(
                    type_=alias.get_data_type_from_section(item)))

        header_section = section.find('VariableLengthHeaderSize')
        try:
            header_size = int(header_section.text.strip())
        except (ValueError, AttributeError):
            header_size = DEFAULT_HEADER_SIZE

        return cls(section.tag, list(args), header_size)

    def create_from_stream(self, stream: BytesIO):
        unpacked_args = []
        unpacked_kwargs = {}
        for arg in self._arguments:
            unpacked = arg.type.create_from_stream(stream, self._variable_header_size)
            if arg.name is None:
                unpacked_args.append(unpacked)
            else:
                unpacked_kwargs[arg] = unpacked

        return unpacked_args, unpacked_kwargs

    def __repr__(self):
        return "{name} ({args})".format(
            name=self._name, args=self._arguments)


class EntityProperty:

    def __init__(self, name, type_: DataType, flags: str, default: etree.ElementBase = None):
        self._name = name
        self._type = type_
        self._default = type_.get_default_value(default)
        self._flags = getattr(EntityFlags, flags)

    def get_name(self):
        return self._name

    def get_size_in_bytes(self):
        return min(self._type.get_size_in_bytes(), INFINITY)

    def get_default_value(self):
        return self._default

    @classmethod
    def from_section(cls, section: etree.ElementBase, alias):
        """
        <ownShipId>
            <Type>ENTITY_ID</Type>
            <Flags>ALL_CLIENTS</Flags>
            <Default>0</Default>
        </ownShipId>
        """

        type_ = alias.get_data_type_from_section(section.find('Type'))
        default = section.find('Default')
        flags = section.find('Flags').text.strip()

        return cls(section.tag, type_, flags=flags, default=default)

    def create_from_stream(self, stream: BytesIO):
        return self._type.create_from_stream(stream)

    def __repr__(self):
        return "{name} ({args})".format(
            name=self._name, args=self._type)


class EntityMethodDescriptions:
    def __init__(self):
        self._internal_index = []
        self._methods_by_name: Dict[EntityMethod] = {}

    def parse(self, section: etree.ElementBase, alias):
        for method in section:
            obj = EntityMethod.from_section(method, alias)
            if obj.get_name() in self._methods_by_name:
                continue
            self._internal_index.append(obj)
            self._methods_by_name[obj.get_name()] = obj

    def get_exposed_index_map(self) -> List[EntityMethod]:
        array = self._internal_index[:]
        array.sort(key=lambda i: i.get_size_in_bytes())
        return array


class EntityPropertiesDescriptions:
    def __init__(self):
        self._internal_index: List[EntityProperty] = []
        self._props_by_name: Dict[EntityProperty] = {}

    def parse(self, section: etree.ElementBase, alias):
        for prop in section:
            obj = EntityProperty.from_section(prop, alias)
            # when same-named properties are in interface
            # and in definition, game client uses last one
            if obj.get_name() in self._props_by_name:
                self._internal_index.remove(self._props_by_name[obj.get_name()])
                self._props_by_name.pop(obj.get_name())
            self._internal_index.append(obj)
            self._props_by_name[obj.get_name()] = obj

    def get_properties_by_flags(self, flags, exposed_index=False) -> List[EntityProperty]:
        props = []
        for prop in self._internal_index:
            if not prop._flags & flags:
                continue
            props.append(prop)

        # client-server index, ordered props by payload size
        if exposed_index:
            props.sort(key=lambda i: i.get_size_in_bytes())
        return props


class BaseDataObjectDef:
    def __init__(self, base_dir: str, alias: Alias):
        self._properties = EntityPropertiesDescriptions()
        self._volatile = {}
        self._alias = alias
        self._base_dir = base_dir

    def _parse_implements(self, implements_list: etree.ElementBase):
        if implements_list is None:
            return

        for it in implements_list:
            path = os.path.join(self._base_dir, ENTITIES_DEFS_PATH, 'interfaces', it.text.strip() + '.def')
            section = etree.parse(path, parser=etree.XMLParser(
                remove_comments=True)).getroot()
            self._parse_section(section)

    def _parse_properties(self, props_list: etree.ElementBase):
        if props_list is None:
            return
        self._properties.parse(props_list, self._alias)

    def _parse_volatile(self, props_list: etree.ElementBase):
        """
        Some properties are updated more often than others,
        and almost all entities have a set of properties that
        need to be handled specially due to this. These properties
        are called volatile properties, and are pre-defined
        by the BigWorld engine.
        <position/> | <position> float </position>
        <yaw/> | <yaw> float </yaw>
        <pitch/> | <pitch> float </pitch>
        <roll/> | <roll> float </roll>
        """
        if props_list is None:
            return

        for item in props_list:
            if item.tag == 'position':
                self._volatile['position'] = (0, 0, 0)
            elif item.tag in ['yaw', 'pitch', 'roll']:
                self._volatile[item.tag] = 0.0

    def _parse_section(self, section: etree.ElementBase):
        self._parse_implements(section.find("Implements"))
        self._parse_properties(section.find("Properties"))
        self._parse_volatile(section.find("Volatile"))


class EntityDef(BaseDataObjectDef):
    """
    This class is used to describe a type of entity. It describes all properties
    and methods of an entity type, as well as other information related to
    object instantiation, level-of-detail etc. It is normally created on startup
    when the entities.xml file is parsed.
    """
    def __init__(self, base_dir:str, name: str, section: etree.ElementBase, alias: Alias):
        self._name = name
        self._cell_methods = EntityMethodDescriptions()
        self._base_methods = EntityMethodDescriptions()
        self._client_methods = EntityMethodDescriptions()

        super(EntityDef, self).__init__(base_dir, alias)

        self._parse_section(section)

    def get_name(self):
        return self._name

    def cell(self):
        return self._cell_methods

    def base(self):
        return self._base_methods

    def client(self):
        return self._client_methods

    def properties(self):
        return self._properties

    def volatiles(self):
        return self._volatile

    def _parse_cell_methods(self, section: etree.ElementBase):
        if section is None:
            return
        self._cell_methods.parse(section, self._alias)

    def _parse_base_methods(self, section: etree.ElementBase):
        if section is None:
            return
        self._base_methods.parse(section, self._alias)

    def _parse_client_methods(self, section: etree.ElementBase):
        if section is None:
            return
        self._client_methods.parse(section, self._alias)

    def _parse_section(self, section: etree.ElementBase):
        super(EntityDef, self)._parse_section(section)
        self._parse_client_methods(section.find("ClientMethods"))
        self._parse_cell_methods(section.find("CellMethods"))
        self._parse_base_methods(section.find("BaseMethods"))
