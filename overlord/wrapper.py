# -*- coding: utf-8 -*-

"""
Created on Apr 19, 2012

@author: quermit
"""

import inspect

import core


def call_stats(func, statistics_manager=None):
    statistics_manager = (statistics_manager
                            or core.StatisticsManager.instance())
    manager = statistics_manager.create_call_stats(
                    inspect.getmodule(func), func)
    return manager.wrap(func)
