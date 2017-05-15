from bs4 import BeautifulSoup
import urllib2
import re

class Urls:
	def call(self, line):
		urls = self.findUrl(line)
		li = list()
		for link in urls:
			soup = BeautifulSoup(urllib2.urlopen(link), "html.parser")
			li.append(soup.title.string)
		return tuple(li)

	def findUrl(self, line):
		return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)