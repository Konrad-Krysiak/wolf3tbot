import unittest
from dictionary import Dictionary
from types import *
import requests
from bs4 import BeautifulSoup
class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.service = Dictionary()

    def test_response_type(self):
        self.assertTrue(type(self.service.requestWord('something')), requests.models.Response )

    def test_rest_call(self):
        result = self.service.call('something')
        self.assertTrue(len(result)>1)
        self.assertEqual(type(result), StringType)

    def test_resonse(self):
		r = requests.get("http://www.dictionary.com/browse/something")
		soup = BeautifulSoup(r.content, "html.parser")
		headword = soup.find("span", attrs={"class":"me"}).text
		self.assertEqual(headword, "something")
if __name__ == '__main__':
    unittest.main()
