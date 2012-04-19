"""
Created on Apr 19, 2012

@author: quermit
"""
import threading

from tornado import web
from tornado import ioloop

import core


def start(address="0.0.0.0", port=8001):
    routing = [
        (r"/", HomeHandler),
        (r"/stats", StatsHandler, dict(
                stats_manager=core.StatisticsManager.instance())),
    ]
    app = web.Application(routing)
    app.listen(port, address)
    t = threading.Thread(target=ioloop.IOLoop.instance().start)
    t.daemon = True
    t.start()


class HomeHandler(web.RequestHandler):
    
    def get(self):
        self.write("Hello world!")


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
        self.write("\n".join(result))
