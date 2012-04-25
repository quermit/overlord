# -*- coding: utf-8 -*-

import inspect
import unittest
import threading

from tornado import web
from tornado import ioloop

from .mox3 import mox
from overlord import core
from overlord import server


class TestStart(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

        self.mox.StubOutWithMock(web, "Application", True)
        self.app_mock = self.mox.CreateMockAnything("application")
        web.Application(
            handlers=mox.IsA(list),
            template_path=mox.Func(lambda a: a.endswith("/templates")),
            static_path=mox.Func(lambda a: a.endswith("/static")),
            ui_methods=mox.Func(lambda m: inspect.ismodule(m)),
            ui_modules=mox.Func(lambda m: inspect.ismodule(m))
        ).AndReturn(self.app_mock)

        self.mox.StubOutWithMock(threading, "Thread", True)
        self.thread_mock = self.mox.CreateMockAnything("thread")
        threading.Thread(target=mox.Func(callable)).AndReturn(self.thread_mock)

    def tearDown(self):
        self.mox.ResetAll()
        self.mox.UnsetStubs()

    def test_creates_app_with_defaults_and_starts_thread(self):
        self.app_mock.listen(8001, "0.0.0.0", io_loop=mox.IsA(ioloop.IOLoop))
        self.thread_mock.daemon = True
        self.thread_mock.start()
        self.mox.ReplayAll()

        server.start()

        self.mox.VerifyAll()

    def test_creates_app_and_starts_thread(self):
        custom_port = 8123
        custom_addr = "192.168.1.1"
        self.app_mock.listen(
                custom_port, custom_addr, io_loop=mox.IsA(ioloop.IOLoop))
        self.thread_mock.daemon = True
        self.thread_mock.start()
        self.mox.ReplayAll()

        server.start(custom_addr, custom_port)

        self.mox.VerifyAll()

    def test_get_routing_returns_valid_handlers(self):
        handlers = server._get_routing()
        routes = [cfg[0] for cfg in handlers]

        self.assertTrue(isinstance(handlers, list))
        self.assertTrue(r"/" in routes)


class HomeHandler(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.handler_mock = self.mox.CreateMock(server.HomeHandler)

    def tearDown(self):
        self.mox.ResetAll()

    def test_handler_renders_index_for_get_request(self):
        self.handler_mock.render("index.html")
        self.mox.ReplayAll()

        server.HomeHandler.get(self.handler_mock)
        self.mox.VerifyAll()


class ResourceUsageHandler(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()
        self.handler_mock = self.mox.CreateMock(server.ResourceUsageHandler)

        self.stats_manager_mock = self.mox.CreateMock(core.StatisticsManager)
        self.stats_manager_mock.resource_usage = self.mox.CreateMockAnything()

        self.handler_mock._stats_manager = self.stats_manager_mock

    def tearDown(self):
        self.mox.ResetAll()

    def test_handler_renders_index_for_get_request(self):
        self.handler_mock.render("resources/index.html",
            resource_usage=self.stats_manager_mock.resource_usage)
        self.mox.ReplayAll()

        server.ResourceUsageHandler.get(self.handler_mock)
        self.mox.VerifyAll()
