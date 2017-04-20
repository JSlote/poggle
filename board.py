#	___  ____ ____ ____ ___  
#	|__] |  | |__| |__/ |  \ 
#	|__] |__| |  | |  \ |__/ .py
#	                         
# This is a model board class that takes care of all the dice and shakes them
# up, just like a real Boggle(TM) board. It also contains a recursive solving
# function.

import random

class Board():
	'''A Poggle Board w/ default size: 4'''
	def __init__(self, dice, wordTree, size = 4):
		'''Initializes the board and shake it'''
		self.size = size
		self.grid = []
		self.dice = dice
		self.wordTree = wordTree
		self.solvedWords = []
		self.shake()

	def __str__(self):
		'''Returns a string containing the grid of letters. Mostly for debugging'''
		val = ""
		for i in range(self.size): # for each row
			for j in range(self.size): # for each column
				val += "%2s" % str(self.grid[j][i]) #add the current char,
				# leaving a space for that nasty 'QU'
			val += "\n" # add a newline for each row
		return val[:-1] #return the grid string and remove the last newline char

	def shake(self):
		'''Rerolls each die and randomizes their positions'''
		#reroll each die in the list of dice
		for die in self.dice:
			die.roll()

		#shuffle the order of the dice in the list
		random.shuffle(self.dice)

		#recast the dice into the grid
		for i in range(self.size):
			self.grid.append([])
			for j in range(self.size):
				self.grid[i].append(self.dice[self.size*(i-1)+j])

		#solve the new board
		self.solvedWords = self.solve(self.wordTree)

	def getDieVal(self,(x,y)):
		'''Returns a string containing the letter at the coordinate.
		x and y start at 0,0'''
		if x < 0 or y < 0:
			raise
		return str(self.grid[x][y]) # makes use of the __str__ method of the dice objects - returns side currently up

	def getSize(self):
		'''Returns the length of one side of the board'''
		return self.size

	def _getPerimList(self,(x,y)):
		'''Returns a list of tuples holding the coords of all adjacent chars to the input coord.
		Helper function for solve()'''
		#throw an error if the input coord is out of range
		self.getDieVal((x,y))

		#make a list to hold the tuples
		coordList = []

		# loop through a 3x3 grid centered on the input coord
		for j in range(y-1, y+2):
			for i in range(x-1, x+2):
				#if the current coord is actually on the board...
				try:
					self.getDieVal((i,j))
				except:
					pass
				else: # then add its coords to the list...
					if i != x or j != y: # providing it's not the input coord.
						coordList.append((i,j))

		return coordList

	def getSolvedWords(self):
		return self.solvedWords

	def solve(self,wordTree):
		'''returns the words available in the current board'''

		# recursive depth-first search algorithm for the words.
		def findWords(self, currCoord, currWordTree, usedCoords, wordList):
			currChar = self.getDieVal(currCoord).upper() # make sure it's all capitalized, specifically the 'Qu'
			if currChar in currWordTree:
				if True in currWordTree[currChar]: #If there is a complete word using the 
				# current char as the last char. 'True' is used as the key if there is a word at the current level.
				# an alternative would be to use a try statement, but I have yet to test
					word = currWordTree[currChar][True] #Second lookup. Would like to avoid this, but luckily look-
					# ups in dicts are lightning.
					if word not in wordList: # if the word hasn't been recorded yet
						wordList.append(word) # add it to the dictionary
				#usedCoords.append(currCoord) # add the char to the usedCoord list
				for coord in self._getPerimList(currCoord):#for all coords around the current char
					if coord not in usedCoords + [currCoord]: #check to make sure the alg isn't retracing its steps:
						#call the function for each char
						findWords(self, coord, currWordTree[currChar], usedCoords+[currCoord], wordList)
			#The base case doen't need to be coded: else: the char's not in current the dictionary. End of function.

		goodWords = [] # make a new list to hold solved words

		for y in range(self.size):
			for x in range(self.size): # starting at each char in the grid of chars, find words.
				findWords(self,(x,y),wordTree,[],goodWords)

		goodWords.sort() # sort the list alphabetically
		return goodWords # return the solved words