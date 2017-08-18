#!/usr/bin/python
# coding=utf-8

from distutils.core import setup

setup(name='BigWorld .def to .py',
      version='1.0',
      description='Python Distribution Utilities',
      author='Oleksandr Shyshatskyi',
      author_email='shalal545@gmail.com',
      packages=['def_generator'],
      scripts=['parse_entities.py'])