#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    redispider.util
    ------------------------------------------------------------

    

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

__all__ = [
    'getItemFromDictList',
    ]

def getItemFromDictList(itemFieldKey, value, dictList):
    for item in dictList:
        if itemFieldKey in item:
            if item[itemFieldKey] == value:
                return item
    return None