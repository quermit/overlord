# -*- coding: utf-8 -*-

import datetime
import unittest

from overlord import core


class TestResourceUsageManager(unittest.TestCase):

    def setUp(self):
        self.manager = core.ResourceUsageManager()

    def test_should_properly_calculate_amount_of_seconds(self):
        days, seconds = 10, 5
        self.manager.initialized_at = (datetime.datetime.now() +
            datetime.timedelta(days=-days, seconds=-seconds))

        uptime = self.manager.uptime

        self.assertEqual(days * 24 * 3600 + seconds, uptime)


if __name__ == "__main__":
    unittest.main()
