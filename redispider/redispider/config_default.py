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
            'port':6379,
            'password':'',
            'db':0,
            },
        #cannot be override
        'key':{
            'main_message':'main_message',
            'master_name':'master_name',
            #init, wait, work, sleep, None
            'master_state':'master_state',
            'slave_name_offline':'slave_name_offline',
            'slave_name_online':'slave_name_online',
            'catalogue_url_set_activated':'catalogue_url_set_activated',
            'catalogue_url_set_deactivated':'catalogue_url_set_deactivated',
            'catalogue_url_list':'catalogue_url_list',
            }
        },
    'multi_process':{
        #0: the cpu core number of your computer
        'max_process':0,
        },
    'master':{
        'reconnection_delay':5,
        'clear_redis_db':True,
        'max_slave_num':100,
        },
    'slave':{
        'reconnection_delay':5,
        }
}