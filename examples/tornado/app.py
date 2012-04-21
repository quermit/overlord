# -*- coding: utf-8 -*-
"""
Created on Apr 20, 2012

@author: quermit
"""
import os
import sys
import time
import random

from tornado import ioloop
from tornado import web

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../..")

import overlord
from overlord import wrapper


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
    port = 5000
    overlord.start()
    application.listen(port)
    print(" * Running on http://127.0.0.1:%d/" % port)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()

