# -*- coding: utf-8 -*-

import unittest
from datetime import timedelta

from overlord import compatibility


class TestTotalSeconds(unittest.TestCase):

    def test_returns_correct_number_of_seconds(self):
        td = timedelta(seconds=123456789)
        
        self.assertEquals(123456789.0, compatibility.total_seconds(td))
