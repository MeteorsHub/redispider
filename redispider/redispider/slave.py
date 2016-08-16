#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    redispider.slave
    ------------------------------------------------------------

    

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import redis
from multiprocessing import process
from multiprocessing import cpu_count


from redispider.config import configs
from redispider.log import Logger


class Slave(object):
    """
        Slave client distributed to slave terminals.
        You should not change configs or create configs_override on slave terminals.
    """

    def __init__(self, host, port=configs.redis.connection.default_port, password=configs.redis.connection.default_password, maxProcess=configs.multi_process.max_process):
        Logger.info('Initiating redispider slave robot...')
        self.host = host
        self.port = port
        self.password = password
        self.maxProcess = self._maxProcess(maxProcess)
        self.runProcess = 1
        self.connect()
        Logger.info('Slave robot created on %s' %self.rds.cli

    def work(self):
        pass

    def connect(self):
        self.connection_pool = redis.Redis.connection_pool(host=self.host, port=self.port, password=self.password)
        self.rds = redis.Redis(connection_pool=self.connection_pool)

    def _maxProcess(self, maxProcess):
        if maxProcess == 0:
            return multiprocessing.cpu_count()
        if not isinstance(maxProcess, int):
            Logger.warning('