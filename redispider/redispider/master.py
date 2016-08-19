#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    redispider.master
    ------------------------------------------------------------

    

    :Copyright (c) 2016 MeteorKepler
    :license: MIT, see LICENSE for more details.

"""

__author__ = 'MeterKepler'

import redis
import time
import subprocess
import os
from multiprocessing import cpu_count, Process
from threading import Thread

from redispider.log import Logger
from redispider.config import configs
from redispider.slave import Slave
from redispider.message import *
from redispider.util import *

class Master(object):
    """
        Master server running on master terminal
    """
    def __init__(self, host, port=configs.redis.connection.port, password=configs.redis.connection.password, db=configs.redis.connection.db, maxProcess=configs.multi_process.max_process):
        Logger.info('Initiating redispider master robot...')
        self.db = db
        self.host = host
        self.port = port
        self.password = password
        self.maxProcess = self.maxProcessCompute(maxProcess)
        self.name = 'master'
        self.runingProcess = 0
        self.slaveList = []
        self.start()

    def start(self):
        Logger.info('Master robot connecting to redis...')
        while True:
            if self.connect():
                break
            time.sleep(configs.master.reconnection_delay)
        Logger.info('Master robot %s created on %s!' %(self.name, self.client_info['addr']))
        self.initMaster()
        Logger.info('Launch main service...')
        try:
            threadMessageLoop = Thread(target=self.messageLoop, args=())
            threadMessageLoop.start()
            self.mainProcess()
                            
        except KeyboardInterrupt:
            Logger.info('Master robot %s shuting down...' %self.name)
        finally:
            self.close()
            threadMessageLoop.join()    
            
            

    def connect(self):
        self.connection_pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password)
        try:
            self.rds = redis.Redis(connection_pool=self.connection_pool)
            if configs.master.clear_redis_db:
                self.rds.flushdb()
            self.rds.set(configs.redis.key.master_name, self.name)
            self.rds.set(configs.redis.key.master_state, 'init')
            self.rds.client_setname(self.name)
            self.client_info = getItemFromDictList('name', self.name, self.rds.client_list())
            return True
        except (TimeoutError, redis.exceptions.ConnectionError):
            Logger.warning('Cannot connect to redis. Please check your connection. ')
            return False

    def initMaster(self):
        for i in range(configs.master.max_slave_num):
            self.rds.lpush(configs.redis.key.slave_name_offline, 'slave%s' %(i + 1))
        self.rds.delete((configs.redis.key.main_message, configs.redis.key.slave_name_online))
        self.rds.set(configs.redis.key.master_state, 'wait')
        self.copyMasterSrc()


    def mainProcess(self):
        
        pass

    def messageLoop(self):
        while True:
            message = fetchMessage(self.rds)
            if message == None:
                continue
            code, msg = message
            if code == 101:
                Logger.info('Slave %s is online' %msg)
                self.slaveList.append(msg)
            if code == 102:
                try:
                    self.slaveList.remove(msg)
                    Logger.info('Slave %s is offline' %msg)
                except ValueError:
                    pass
                    Logger.warning('Slave %s is going offline but it was not online at all.' %msg)


    def copyMasterSrc(self):
        Logger.info('Copy configs and code to redis...')
        pass

    def maintainSlave(self):
        pass


    

    def close(self):
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