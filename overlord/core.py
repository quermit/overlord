# -*- coding: utf-8 -*-

"""
Created on Apr 19, 2012

@author: quermit
"""

import functools, time, logging
from collections import deque

# XXX: this is strange, because user logging in flask test app is turned on
#      after reaching localhost:8001/logs URL
class OverlordLogger(logging.getLoggerClass()):
    
    @property
    def _manager(self):
        if not hasattr(self, "__manager"):
            self.__manager = StatisticsManager.instance()            
        
        return self.__manager

    def handle(self, record):
        self._manager.logs.append(record)
        return super(OverlordLogger, self).handle(record)

class StatisticsManager(object):
    
    def __init__(self):
        self.call_stats = []
        self.logs = []

        logging.setLoggerClass(OverlordLogger)
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
    
    def create_call_stats(self, module, function):
        stats = _CallStatistics(self, module, function)
        self.call_stats.append(stats)
        return stats
    
class Wrapper(object):
    def wrap(self, function):
        raise NotImplementedError

class _CallStatistics(Wrapper):
    """
        TODO: since we would like to have call-stack like statiscs, it would be
              nice to have one instance of _CallStatistics per usage:
                one global and each for one call-stack
              it will allow to see global stats and fine grained stats for
              each distinct traceback
        
        XXX: what about recursive functions?
    """
    _TIME_CONST = 0.01
    
    def __init__(self, manager, module, function):
        self.manager = manager

        self.module = module
        self.function = function
        self.min_time = None
        self.max_time = None
        self.avg_time = None
        self.calls = 0
        self.errors = 0
    
    def add_success(self, exec_time):
        self.calls += 1
        if self.calls == 1:
            self.min_time, self.max_time, self.avg_time = [exec_time] * 3
            return
        self.min_time = min(self.min_time, exec_time)
        self.max_time = max(self.max_time, exec_time)
        self.avg_time = self._exp_mov_avg(
                self.avg_time, exec_time, self._TIME_CONST)
        print "%s %s %s" % (self.min_time, self.max_time, self.avg_time)
    
    def add_failure(self, exception):
        self.calls += 1
        self.errors += 1
        
    def _exp_mov_avg(self, curr_val, next_val, time_const):
        return (1.0 - time_const) * curr_val + time_const * next_val
    
    def wrap(self, function):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = function(*args, **kwargs)
                self.add_success(time.time() - start_time)
                return result

            except Exception, e:
                self.add_failure(e)
                raise

        return wrapper
