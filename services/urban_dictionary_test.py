import unittest
from urban_dictionary import UrbanDictionary
from types import *
import json

class TestUrbanDictionary(unittest.TestCase):

    def setUp(self):
        self.service = UrbanDictionary()

    def test_response_type(self):
        self.assertTrue(type(self.service.requestWord('something')), StringType )

    def test_json_parsing(self):
        self.assertTrue(type(json.loads(self.service.requestWord('something'))), DictType )

    def test_resonse(self):
        word = 'something'
        response_json = json.loads(self.service.requestWord(word))
        self.assertEqual(word, response_json['list'][0]['word'])

    def test_rest_call(self):
        result = self.service.call('something')
        self.assertTrue(len(result)>1)
        self.assertEqual(type(result), StringType)


if __name__ == '__main__':
    unittest.main()
