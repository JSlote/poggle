#	___  _ ____ ____ ___  _ ____ _  _ _    ____ ____ 
#	|  \ | |    |___ |__] | |    |_/  |    |___ |__/ 
#	|__/ | |___ |___ |    | |___ | \_ |___ |___ |  \ .py
#	                                                 
# This script pickles a list of dice objects using authentic dice sequences
# taken directly from the Boggle(TM) board.

import die
import cPickle as pickle

print "Pickling dice..."

diceSeqs = [ # The real stuff.
["D","T","N","K","U","O"],
["P","E","C","A","D","M"],
["H","I","S","E","N","P"],
["L","S","P","T","U","E"],
["L","I","B","A","Y","T"],
["U","G","I","R","W","L"],
["A","C","O","T","I","A"],
["H","R","S","M","O","A"],
["A","N","E","D","Z","V"],
["E","C","A","S","R","L"],
["W","N","S","D","E","O"],
["O","F","I","R","B","X"],
["K","U","L","E","G","Y"],
["Qu","J","M","B","A","O"],
["E","N","I","G","T","V"],
["E","E","I","Y","H","F"]]

dieList = []

for i in range(len(diceSeqs)): # for each sequence, create a dice object
	dieList.append(die.Die(diceSeqs[i]))

#Pickle the list of die objects
pickle.dump(dieList,open("dielist.list", "wb"),-1)# the -1 means most modern protocol. Change to 2 if experiencing issues

print "Process Complete"