# -*- coding: utf-8 -*-

import sys, unittest

import sys, os
the_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, the_root)

from overlord import wrapper
from overlord.core import StatisticsManager

class TestCallStatsWrapper(unittest.TestCase):
    def setUp(self):
        self.manager = StatisticsManager.instance()
        self.manager.call_stats = []

    def test_should_add_one_to_call_counter(self):
        # given
        wrapped_function = wrapper.call_stats(lambda: 123)

        # when
        result = wrapped_function()

        # then
        self.assertEqual(123, result)
        self.assertEqual(1, self.manager.call_stats[-1].calls)

