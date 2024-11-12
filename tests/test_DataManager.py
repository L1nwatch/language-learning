#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

from unittest import TestCase
from DataManager import DataManager

if __name__ == "__main__":
    pass


class TestDataManager(TestCase):
    def setUp(self) -> None:
        self.dm = DataManager()

    def test_load_cases(self):
        result = self.dm.load_cases()
        self.assertIsInstance(result, list)
        if len(result) > 0:
            self.assertIsInstance(result[0], dict)
            self.assertIn("file", result[0])
            self.assertIn("answer", result[0])
            self.assertIn("type", result[0])
            self.assertIn("start_time", result[0])
            self.assertIn("end_time", result[0])
