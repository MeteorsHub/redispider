#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    setup.py
    ------------------------------------------------------------

    A setup tool for installing redispider to your computer.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'


from distutils.core import setup

setup(name='redispider',
      version='0.1.0',
      description='A distributed spider based on redis and espider',
      author='MeteorKepler',
      author_email='JimRanor@outlook.com',
      packages=['redispider'],
    )