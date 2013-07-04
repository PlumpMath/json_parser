import unittest
import json
from parse import loads


class JsonParseTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_hash(self):
        expected = {}
        string = json.dumps(expected)
        actual = loads(string)
        self.assertDictEqual(expected, actual)

    def test_simple_hash(self):
        string = '{"key":"value"}'
        expected = json.loads(string)
        actual = loads(string)
        self.assertDictEqual(expected, actual)

    def test_hash_incomplete(self):
        string = '{"key'
        self.assertRaises(ValueError, loads, string)

    def test_hash_missing_colon(self):
        string = '{"key""value"}'
        self.assertRaises(ValueError, loads, string)

    def test_string_with_tick(self):
        string = '{"key":\'value\'}'
        self.assertRaises(ValueError, loads, string)

    def test_hash_with_int(self):
        string = '{"int":101}'
        expected = json.loads(string)
        actual = loads(string)
        self.assertDictEqual(expected, actual)

    def test_hash_nested(self):
        string = '{"hash":{"inception":"win"}}'
        expected = json.loads(string)
        actual = loads(string)
        self.assertDictEqual(expected, actual)