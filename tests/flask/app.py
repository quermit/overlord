# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../..")


import time, traceback
from flask import Flask, request
app = Flask(__name__)

from overlord import server, wrapper


@wrapper.call_stats
def time_consuming_function():
    time.sleep(1)

# XXX: adding decorator on top will not cause stats to update
# @wrapper.call_stats
@app.route("/")
@app.route("/user/<username>")
@wrapper.call_stats
def hello(username="World"):
    time_consuming_function()
    return "Hello %(username)s!" % locals()

if __name__ == "__main__":
    server.start()
    app.run()