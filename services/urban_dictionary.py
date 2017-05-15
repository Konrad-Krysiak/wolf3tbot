import requests
import json
import os

class UrbanDictionary:
    def call(self, word):
        response = json.loads(self.requestWord(word))
        try:
        	term = str(response["list"][0]["definition"])
        except:
        	return "^1Urban: ^7No definition for {} yet. Sorry!".format(word)
        filtered = os.linesep.join([s for s in term.splitlines() if s]) # Remove \n(new lines). Necessary to print definitions in game.
        term = ' '.join(filtered.splitlines())
        return "^1Urban: ^7{}".format(term)
        
    def requestWord(self, word):
        return requests.get("http://api.urbandictionary.com/v0/define?term={}".format(word)).content
        