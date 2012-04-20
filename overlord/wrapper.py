# -*- coding: utf-8 -*-

"""
Created on Apr 19, 2012

@author: quermit
"""

import inspect
import core

def call_stats(func):
    # XXX: I don't like the singleton pattern here :( it is hard to test
    manager = core.StatisticsManager.instance().create_call_stats(
            inspect.getmodule(func), func)
    return manager.wrap(func)
