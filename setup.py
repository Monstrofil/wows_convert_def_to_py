#!/usr/bin/python
# coding=utf-8
from setuptools import setup

setup(
    name='BigWorld .def to .py',
    version='1.1',
    description='Python Distribution Utilities',
    author='Oleksandr Shyshatskyi',
    author_email='shalal545@gmail.com',
    license='MIT',
    packages=['def_generator', 'def_generator.entities'],
    package_data={'': ['*.j2', '*.py']},
    include_package_data=True,
    scripts=['parse_entities.py'],
)
