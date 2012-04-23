# -*- coding: utf-8 -*-

"""
Created on Apr 19, 2012

@author: quermit, dejw
"""

import collections
import datetime
import functools
import gc
import getpass
import logging
import os
import sys
import resource
import time
import threading


# XXX(dejw): this is strange, because user logging in flask test app is turned
#   on after reaching localhost:8001/logs URL
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
        self.resource_usage = ResourceUsageManager()

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
        TODO(dejw): since we would like to have call-stack like statiscs, it
            would be nice to have one instance of _CallStatistics per usage:
            one global and each for one call-stack; it will allow to see global
            stats and fine grained stats for each distinct traceback

        XXX(dejw): what about recursive functions?
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

            except Exception as e:
                self.add_failure(e)
                raise

        return wrapper


class ResourceUsageManager(object):

    def __init__(self):
        self.initialized_at = datetime.datetime.now()

    @property
    def command_line_args(self):
        return sys.argv

    @property
    def thread_count(self):
        return threading.active_count()

    @property
    def uptime(self):
        delta = (datetime.datetime.now() - self.initialized_at)
        return int(delta.total_seconds())

    @property
    def gc_enabled(self):
        return gc.isenabled()

    @property
    def gc_count(self):
        return gc.get_count()

    @property
    def gc_threshold(self):
        return gc.get_threshold()

    @property
    def created_objects(self):
        """Generates a statistics of created objects.

        Returns:
            A list of tuples (klass, count), sorted in descending order of
            count.
        """

        objects = gc.get_objects()
        counts = collections.defaultdict(lambda: 0)

        for object_ in objects:
            object_type = type(object_)

            # XXX(dejw): inspect.isbuiltin(object_) seems to not working
            is_builtin = (object_type.__module__ == '__builtin__')
            if not is_builtin and not object_type.__module__.startswith("_"):

                full_name = "%s.%s" % (object_type.__module__,
                                       object_type.__name__)
                counts[full_name] += 1

        return sorted(counts.items(), key=lambda x: x[1], reverse=True)

    @property
    def cwd(self):
        return os.getcwd()

    @property
    def uid(self):
        return os.getuid()

    @property
    def login(self):
        return getpass.getuser()

    @property
    def gid(self):
        return os.getgid()

    @property
    def pid(self):
        return os.getpid()

    @property
    def rusage(self):
        """
        Returns:
            A dict representing rusage structure only for current proces.
        """

        rusage_struct = resource.getrusage(resource.RUSAGE_SELF)
        fields = [f for f in dir(rusage_struct) if not f.startswith("_")]

        rusage = {}
        for field in fields:
            rusage[field] = getattr(rusage_struct, field)

        return rusage
