#!/usr/bin/python
# coding=utf-8
from entities.entities_constructor import EntitiesConstructor

__author__ = "Aleksandr Shyshatsky"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-path', type=str, help='path to folder that contains "scripts"')
    namespace = parser.parse_args()

    constructor = EntitiesConstructor(namespace.base_path)
    constructor.build_entities()
