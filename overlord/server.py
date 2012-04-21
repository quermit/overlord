# -*- coding: utf-8 -*-
"""
Created on Apr 19, 2012

@author: quermit
"""
import os
import threading
import logging

from tornado import web
from tornado import ioloop

from . import core


def start(address="0.0.0.0", port=8001):
    data = dict(stats_manager=core.StatisticsManager.instance())

    handlers = [
        (r"/", HomeHandler),
        (r"/logs", LoggingHandler, data),
        (r"/logs/(.*)", LoggingHandler, data),
        (r"/stats", StatsHandler, data),
    ]

    separate_ioloop = ioloop.IOLoop()
    
    app = web.Application(
            handlers=handlers,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"))
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
        result = []
        for stats in self._stats_manager.call_stats:
            result.append("%s :: %s" % (
                    stats.module.__name__, stats.function.__name__))
            result.append("  calls: %d / errors: %d" % (
                    stats.calls, stats.errors))
            if stats.calls > 0:
                result.append("  time: %.3f / %.3f / %.3f" % (
                        stats.min_time, stats.max_time, stats.avg_time))
        self.write("<br/>\n".join(result))
