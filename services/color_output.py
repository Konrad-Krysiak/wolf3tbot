import string
import random

class ColorOutput:
	def call(self, string):
	    return ''.join(["^" + self.color_generator() + a for a in string])
	def color_generator(self, chars=string.ascii_uppercase):
	    return random.choice(chars)