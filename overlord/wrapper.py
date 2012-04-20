"""
Created on Apr 19, 2012

@author: quermit
"""
import time
import inspect

from functools import wraps

import core


def call_stats(func):
    # XXX: I don't like the singleton pattern here :( it is hard to test
    manager = core.StatisticsManager.instance().create_call_stats(
            inspect.getmodule(func), func)
    @wraps(func)
    def wrapper(*args, **kwards):
        start_time = time.time()
        try:
            result = func(*args, **kwards)
            manager.add_success(time.time() - start_time)
            return result
        except Exception, e:
            manager.add_failure(e)
            raise
    return wrapper
