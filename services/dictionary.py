import requests
from bs4 import BeautifulSoup

class Dictionary:
	def call(self, word):
		soup = BeautifulSoup(self.requestWord(word).content, "html.parser")
		try:
			term_meaning = soup.find("div", attrs={"class":"def-content"}).text
		except:
			return "^1Define: ^7No definition for {} yet. Sorry!".format(word)
		encoded_dict_term = term_meaning.encode('ascii', 'ignore')
		term_meaning = ' '.join(encoded_dict_term.split())
		return "^1Define: ^7{}".format(term_meaning)
	def requestWord(self, word):
		return requests.get("http://www.dictionary.com/browse/{}".format(word))
		