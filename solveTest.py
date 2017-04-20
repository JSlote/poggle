#	____ ____ _    _  _ ____ ___ ____ ____ ___ 
#	[__  |  | |    |  | |___  |  |___ [__   |  
#	___] |__| |___  \/  |___  |  |___ ___]  |  .py
#	                                           
# This is just a simple test of the solving algorithm.

import cPickle as pickle
import random
import board

#random.seed(13)

#checks whether there's a list of dice. If there isn't, it makes one.
try:
	dieList = pickle.load(open("dielist.list", "rb"))
except:
	import dicePickler
	dieList = pickle.load(open("dielist.list", "rb"))

#checks whether there's a wordTree. If there isn't, it makes one.
try:
	wordTree = pickle.load(open("words.tree", "rb"))
except:
	import wordPickler
	wordTree = pickle.load(open("words.tree", "rb"))

#Enter a loop
while True:
	theBoard = board.Board(dieList,wordTree)
	print str(theBoard)
	goodwords = theBoard.solve(wordTree)
	print "I found",len(goodwords),"words!"
	i = 0
	for word in goodwords:
		print "%16s" % word,
		i+=1
		if i%5 == 0:
			print
	theBoard.shake()
	raw_input("")