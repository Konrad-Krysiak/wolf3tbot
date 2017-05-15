import socket_client as SC

class Authenticator:
	def authenticate(self, line):
		UDPnames = SC.get_names()
		nickList = self.parseNames(line)
		auth = [i for i in nickList if i in UDPnames]
		if auth:
			return auth[0]	

	def parseNames(self, line):
		groups = line.split(':')
		nickList = list()
		for x in range(line.count(":")):
			nickList.append(':'.join(groups[:x+1]))
		return nickList

