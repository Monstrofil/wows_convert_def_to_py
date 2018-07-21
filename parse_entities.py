#!/usr/bin/python
# coding=utf-8
from def_generator.entities import EntitiesConstructor

__author__ = "Aleksandr Shyshatsky"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-path', type=str, required=True,
                        help='path to folder that contains "scripts"')
    namespace = parser.parse_args()

    constructor = EntitiesConstructor(namespace.base_path)
    constructor.build_entities()
