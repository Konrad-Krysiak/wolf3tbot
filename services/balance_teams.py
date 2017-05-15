import random
import socket_client as SC
import re

class BalanceTeams:
	def call(self, *args):
		axis, allies, data = self.get_teams_info()
		if axis-allies > 2:
			index = self.get_random_index(map(int, data), lambda x: x==1)
			return "!putteam "+ SC.get_names()[index] + " b"
		elif allies-axis > 2:
			index = self.get_random_index(map(int, data), lambda x: x==2)
			return "!putteam "+ SC.get_names()[index] + " r"
		else:
			return "^1[^7balanceteams^1]^s Teams are balanced."

	def get_random_index(self, seq, pred=lambda: True):
		indexes = [index for index, elem in enumerate(seq) if pred(elem)]
		return random.choice(indexes)

	def get_teams_info(self):
		data = SC.connect_to_server()[1]
		team_variables = re.search(r'P\\(.*)\\vote', data).group(1)
		team_variables = team_variables.replace("-", "")
		axis = team_variables.count("1")
		allies = team_variables.count("2")
		return [axis, allies, team_variables]
