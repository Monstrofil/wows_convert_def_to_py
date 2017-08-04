#!/usr/bin/python
# coding=utf-8
__author__ = "Aleksandr Shyshatsky"


class Entity(object):
    """
    Base entity implementation;
    Used in constructor and during template rendering;
    """
    def __init__(self, name):
        self.name = name
        self.methods = []
