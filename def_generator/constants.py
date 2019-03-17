#!/usr/bin/python
# coding=utf-8
import logging

__author__ = "Aleksandr Shyshatsky"

logging.basicConfig(
    level=logging.DEBUG,
)


class EntityFlags:
    """
    This enumeration is used for flags to indicate properties of data associated
    with an entity type.
    """
    # public flags
    CELL_PRIVATE        = 0
    CELL_PUBLIC         = 1
    OTHER_CLIENTS       = 2
    OWN_CLIENT          = 4
    BASE                = 8
    BASE_AND_CLIENT     = 16
    CELL_PUBLIC_AND_OWN = 32
    ALL_CLIENTS         = 64
    EDITOR_ONLY         = 128


aliasesFile: str = "scripts/entity_defs/alias.xml"

# entities constants

entitiesFile: str = "scripts/entities.xml"

ENTITIES_DEFS_PATH: str = "scripts/entity_defs"

# user data objects constants

userDataObjectsFile: str = "scripts/user_data_objects.xml"

userDataObjectsDefsPath: str = "scripts/user_data_object_defs"

INFINITY = 0xFFFF

