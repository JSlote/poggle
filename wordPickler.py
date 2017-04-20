#	_ _ _ ____ ____ ___  ___  _ ____ _  _ _    ____ ____ 
#	| | | |  | |__/ |  \ |__] | |    |_/  |    |___ |__/ 
#	|_|_| |__| |  \ |__/ |    | |___ | \_ |___ |___ |  \ .py
#	                                                     
# This script loads a list of all the officially useable Scrabble(TM) words and
# puts them in a tree in which each level is a character in the word. This tree
# is made from dictionaries of dictionaries of ... of dictionaries. It is then 
# pickled to words.tree. This file should be only run once, on new installs of 
# the game.

import cPickle as pickle

print "Pickling word list..."

#Recursive function to append words to dictionary
def dictAppender(charList,dictionary,wordpermanent):

	#base case: the word has reached an end
	if len(charList) == 0:
		dictionary[True] = wordpermanent #add an entry at the current pos that looks like True:"word"
		return dictionary #return this base dictionary up through the dictionaries
	
	#keep reading down the word
	else:
		char = charList[0]
		if char == "Q": # deals with the fact that Poggle has no dice w/ just a "Q" character
			char = "QU"
		if char in dictionary: # if it's the char's already in there, don't make a new dictionary
			dictionary[char] = dictAppender(charList[len(char):],dictionary[char],wordpermanent) #call the function again,
			# taking care to remove 2 chars from the beginning of the list if char is QU
			return dictionary
		else:
			dictionary[char] = {} # make a new dictionary to be the char key's value
			# go through the algorithm for all the rest of the chars in the word
			dictionary[char] = dictAppender(charList[len(char):],dictionary[char],wordpermanent) #call the function again,
			# taking care to remove 2 chars from the beginning of the list if char is QU
			return dictionary

#Word list is the Enable list, in the Public Domain. http://www.puzzlers.org/dokuwiki/doku.php?id=solving:wordlists:about:start
wordFile = open("words.txt", "r")
words = wordFile.readlines()
dictionary = {}

for word in words:
	word = word.strip().upper()
	if len(word) >2 and len(word) < 17:
		#print len(word),
		dictionary = dictAppender(word,dictionary,word)
		#print word
		#raw_input("")

pickle.dump(dictionary, open("words.tree", "wb"),-1) # the -1 means most modern protocol. Change to 2 if experiencing issues
print "Process Complete"