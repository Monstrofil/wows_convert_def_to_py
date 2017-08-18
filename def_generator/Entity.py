#!/usr/bin/python
# coding=utf-8
__author__ = "Aleksandr Shyshatsky"


class Entity(object):
    def __init__(self):
        self.id = None
        self.position = None

    def __repr__(self):
        return "<{}> {}".format(self.__class__.__name__, self.__dict__)