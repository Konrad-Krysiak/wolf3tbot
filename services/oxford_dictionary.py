import requests
import json
import os

class Definitions:
	def __init__(self):
		self.app_id = '668335d1'
		self.app_key = 'c643953061bb5515949871e56bc4d229'
		self.language = 'en'

	def call(self, word_id):
		response = json.loads(self.requestWord(word_id).content)
		try:
			result = str(response['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0])
		except:
			return "^1Oxford: ^7No definition for {} yet. Sorry!".format(word)
		return "^1Oxford:  ^7{}".format(result)

	def requestWord(self, word_id):
		url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + self.language + '/' + word_id.lower() +'/definitions'
		return requests.get(url, headers = {'app_id': self.app_id, 'app_key': self.app_key})

		
	