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
import time
from multiprocessing import process
from multiprocessing import cpu_count


from redispider.config import configs
from redispider.log import Logger
from redispider.message import *
from redispider.util import *


class Slave(object):
    """
        Slave client distributed to slave terminals.
        You should not change configs or create configs_override on slave terminals.
    """

    def __init__(self, host, port=configs.redis.connection.port, password=configs.redis.connection.password, db=configs.redis.connection.db, maxProcess=configs.multi_process.max_process):
        Logger.info('Initiating redispider slave robot...')
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.maxProcess = self.maxProcessCompute(maxProcess)
        self.runingProcess = 0
        self.start()

    def start(self):
        while True:
            if self.connect():
                break
            time.sleep(configs.slave.reconnection_delay)
        Logger.info('Slave robot %s created on %s! Work for master %s...' %(self.name, self.client_info['addr'], self.masterName))
        Logger.info('Launch main service...')
        try:
            while True:
                self.mainService()
        except KeyboardInterrupt:
            Logger.info('Slave robot %s shuting down...' %self.name)
        finally:
            self.close()


    def mainService(self):
        
        pass

    def connect(self):
        self.connection_pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password)
        try:
            self.rds = redis.Redis(connection_pool=self.connection_pool)
            masterState = self.rds.get(configs.redis.key.master_state).decode('utf8')
            if masterState == None:
                Logger.warning('Cannot connect to master. Try another time...')
                return False
            if masterState == 'init':
                Logger.warning('Master is initiating. Waiting until it is done...')
                return False
            if masterState == 'sleep':
                Logger.warning('Master is sleeping. Waiting until it wake up...')
                return False
            self.name = self.rds.rpoplpush(configs.redis.key.slave_name_offline, configs.redis.key.slave_name_online).decode('utf8')
            self.rds.client_setname(self.name.encode('utf8'))
            self.client_info = getItemFromDictList('name', self.name, self.rds.client_list())
            self.masterName = self.rds.get(configs.redis.key.master_name).decode('utf8')
            if self.name == None:
                Logger.info('Master does not need more slave! Slave will be shutdown...')
                exit(0)
            sendMessage(101, self.name, self.rds)
            return True
        except (TimeoutError, redis.exceptions.ConnectionError):
            Logger.warning('Cannot connect to redis. Please check your connection. ')
            return False
        
    def close(self):
        sendMessage(102, self.name, self.rds)
        self.rds.client_kill(self.client_info['addr'])
        

    def maxProcessCompute(self, maxProcess):
        cpu = cpu_count()
        if maxProcess == 0:
            return cpu
        if not isinstance(maxProcess, int):
            Logger.warning('max_process in configs is not an integer. Redispider will use default configs.')
            return cpu
        if maxProcess < 0:
            Logger.warning('max_process should be larger than 0. Redispider will use default configs.')
            return cpu
        return maxProcess