# -*- coding: utf-8 -*-
"""
Created on Apr 20, 2012

@author: quermit
"""

import sys
import time
import random

from tornado import ioloop
from tornado import web

import server
import wrapper


def some_time_consuming_function(amount):
    time.sleep(amount)


class MainHandler(web.RequestHandler):

    @wrapper.call_stats
    def get(self):
        some_time_consuming_function(random.random() * 3.0)
        self.write("Boom!")


application = web.Application([
    (r"/", MainHandler),
], debug=True)


def run():
    server.start()
    application.listen(int(sys.argv[1]))
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    run()
