#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    redispider.config_default.py
    ---------------------------------------------------------------------------------------

    Set up default config, if you wan't to change some configs, please do so in 
    config_override.py in your project path.

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeteorKepler'

__all__ = [
    'configs',
    ]

configs = {
    'logging':{
        'level':'INFO',
        'filelog':True,
        'formatter_style':0,
        'filename':'resources/espider.log',
        'filemode':'a',
    },
    'redis':{
        'connection':{
            'default_port':6379,
            'default_password':'',
            },
        'key':{
            'logger':'logger',
            }
        },
    'multi_process':{
        #If 0 be the cpu core number of your computer
        'max_process':0,
        },
    'slave':{
        
        }
}