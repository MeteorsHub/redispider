#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    redispider.message
    -----------------------------------------------------------

   
    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import redis

from redispider.config import configs

__all__ = [
    'MESSAGE_CODE',
    'sendMessage',
    'joinMessage',
    'fetchMessage',
    'splitMessage',
    ]

MESSAGE_CODE = [
    # slave online
    101,
    # slave offline
    102,
    ]

def sendMessage(code, msg, rds):
    if not isinstance(rds, redis.client.Redis):
        return None
    message = joinMessage(code, msg)
    try:
        rds.lpush(configs.redis.key.main_message, message.encode('utf8'))
        return message
    except Exception:
        return None

def joinMessage(code, msg):
    if code not in MESSAGE_CODE:
        return None
    if not isinstance(msg, str):
        return None
    return '%s:%s' %(code, msg)

def fetchMessage(rds):
    if not isinstance(rds, redis.client.Redis):
        return None
    message = rds.rpop(configs.redis.key.main_message)
    if message != None:
        message = message.decode('utf8')
    return splitMessage(message)

def splitMessage(message):
    if not isinstance(message, str):
        return None
    code, msg = message.split(':')
    code = int(code)
    return (code, msg)