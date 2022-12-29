# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import reference1


class RedisUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.max_data = 100000
        self.host = 'localhost'
        self.port = 6379
        self.data = {'id': 1234_0, 'url': 'google.com', 'lang': 'ko', 'keywords': 'hahaha\test'}

    def test_01_put_dict_to_queue(self):
        for _ in range(2):
            result = reference1.put_raw_data_to_queue(self.data)
            print(result)

    def test_02_get_dict_from_queue(self):
        for _ in range(3):
            result = reference1.get_json_data_from_queue()
            print(result)
            print(type(result))