import random
import socket_client as SC

class Sexy:
	def call(self, *args):
		return "^3Obviously ^7{}^3 is sexy!".format(random.choice(SC.get_color_names()))
