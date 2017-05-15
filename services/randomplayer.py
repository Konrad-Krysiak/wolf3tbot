import random
import socket_client as SC
import re

class RandomPlayer:
	def call(self, args=None):
		if args == "r":
			team_variables = self.get_teams_info()
			index = self.get_index(map(int, team_variables), lambda x: x==1)
			return "^3-----^7{}^3-----".format(SC.get_color_names()[index])
		elif args == "b":
			team_variables = self.get_teams_info()
			index = self.get_index(map(int, team_variables), lambda x: x==2)						
			return "^3-----^7{}^3-----".format(SC.get_color_names()[index])
		elif args == "s":
			team_variables = self.get_teams_info()
			index = self.get_index(map(int, team_variables), lambda x: x==3)
			return "^3-----^7{}^3-----".format(SC.get_color_names()[index])
		else:
			return "^3-----^7{}^3-----".format(random.choicez(SC.get_color_names()))

	# def get_index(li, elem):
	# index_list = [index for index in range(len(li)) if li[index] == element]
	# return random.choice(index_list)

	def get_index(self, seq, pred=lambda: True):
		indexes = [index for index, elem in enumerate(seq) if pred(elem)]
		return random.choice(indexes)

	def get_teams_info(self):
		data = SC.connect_to_server()[1]
		team_variables = re.search(r'P\\(.*)\\vote', data).group(1)
		team_variables = team_variables.replace("-", "")
		return team_variables