# -*- coding: utf-8 -*-

import os
import sys
import unittest

from overlord import wrapper
from overlord import core


class TestCallStatsWrapper(unittest.TestCase):

    def test_should_add_one_to_call_counter(self):
        manager = core.StatisticsManager()
        wrapped_function = wrapper.call_stats(lambda: 123,
                statistics_manager=manager)

        result = wrapped_function()

        self.assertEqual(123, result)
        self.assertEqual(1, manager.call_stats[-1].calls)


if __name__ == "__main__":
    unittest.main()
