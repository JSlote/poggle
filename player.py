#	___  _    ____ _   _ ____ ____ 
#	|__] |    |__|  \_/  |___ |__/ 
#	|    |___ |  |   |   |___ |  \ .py
#	                               
# This model class defines a generic player with an ability to calculate its
# own score after adding words to its own list.

class Player():
	def __init__(self):
		'''Initialize the object - no input necessary'''
		self.foundWords = []
		self.score = 0
	def addWord(self, word, goodWords):
		'''addWord takes the current word and checks it against the other input,
		the list of words in the Poggle board. If the word is actually on the
		board, it adds it its list.'''
		if word not in self.foundWords and word in goodWords:
			self.foundWords.append(word)
			self.foundWords.sort() # sort the player's list for asthetic purposes
	def reset(self):
		'''Re-initialize object'''
		# basic reset function is just like __init__()
		self.foundWords = []
		self.score = 0
	def calcScore(self):
		''' Go through the player's list and calculate its score based on
		num of chars word - 2 for each word'''
		for word in self.foundWords:
			self.score += len(word)-2
		return self.score
	def outputWords(self):
		'''Returns a string containing a list of all the words currently in the
		player's list'''
		words = ""
		for word in self.foundWords:
			words += word +"\n"
		return words