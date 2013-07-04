import unittest
import json
from parse import loads


class JsonParseTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hash_happy_path(self):
        expected = {}
        string = json.dumps(expected)
        actual = loads(string)
        self.assertDictEqual(expected, actual)
