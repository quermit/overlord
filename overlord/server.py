# -*- coding: utf-8 -*-
"""
Created on Apr 19, 2012

@author: quermit
"""

import logging
import os
import threading
import re

from tornado import web
from tornado import ioloop

from . import core
from . import helpers
from . import uimodules


def _get_routing():
    data = dict(stats_manager=core.StatisticsManager.instance())
    return [
        (r"/", HomeHandler),
        (r"/logs", LoggingHandler, data),
        (r"/logs/(.*)", LoggingHandler, data),
        (r"/stats", StatsHandler, data),
        (r"/resources", ResourceUsageHandler, data),
    ]


def start(address="0.0.0.0", port=8001):
    separate_ioloop = ioloop.IOLoop()
    app = web.Application(
            handlers=_get_routing(),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_methods=helpers,
            ui_modules=uimodules)

    app.listen(port, address, io_loop=separate_ioloop)

    t = threading.Thread(target=separate_ioloop.start)
    t.daemon = True
    t.start()


class HomeHandler(web.RequestHandler):

    def get(self):
        self.render("index.html")


class LoggingHandler(web.RequestHandler):

    def initialize(self, stats_manager):
        self._stats_manager = stats_manager

    def get(self, level=None):
        if not level:
            self.write({
                'logs': [logging.LogRecord.getMessage(m)
                         for m in self._stats_manager.logs]
            })

        else:
            level = int(level)
            logging.getLogger().setLevel(level)
            self.write({'level': logging.getLevelName(level)})


class StatsHandler(web.RequestHandler):

    def initialize(self, stats_manager):
        self._stats_manager = stats_manager

    def get(self):
        """ GET /stats """

        stats = []
        for stat in self._stats_manager.call_stats:
            endpoint = "%s.%s" % (stat.module.__name__, stat.function.__name__)

            stats.append((endpoint, stat.calls, stat.errors, stat.min_time,
                          stat.avg_time, stat.max_time))

        self.render('callstats/index.html', stats=stats)


# TODO: maybe move this class, in the same module where ResourceUsageManager
#       lies? in this way, managers will be pretty independent (plugins?)
class ResourceUsageHandler(web.RequestHandler):

    def initialize(self, stats_manager):
        self._stats_manager = stats_manager

    def get(self):
        """ GET /resources """
        self.render('resources/index.html',
            resource_usage=self._stats_manager.resource_usage)
