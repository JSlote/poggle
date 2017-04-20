#	___  _ ____ 
#	|  \ | |___ 
#	|__/ | |___ .py
#	            
# This class describes a simple die - it can be rolled
# and return its top side

import random

class Die():
	def __init__(self,seq):
		self.sides = seq
		self.roll()
	def __str__(self): # str(die) will return the current sideup
		return self.sideUp
	def roll(self):
		self.sideUp = self.sides[random.randrange(6)]
		return self.sideUp # return the new side