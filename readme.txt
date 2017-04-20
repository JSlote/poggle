Addendum, 2017: I wrote this as a final project for my Intro to CS class at Carleton
College in 2012. Looking back I see a number of things that should change, but I'm
not sure the world really needs a TKinter Boggle implementation at the moment. That
being said, it is probably the most thoroughly (overly?) documented such program, so
maybe someone will find it of use.                                              --JS

	
	___  ____ ____ ____ _    ____ 
	|__] |  | | __ | __ |    |___ 
	|    |__| |__] |__] |___ |___ 
	    It's Python Boggle!

Overview:
Poggle simulates a Boggle(TM) game against a computer opponent. It features an
efficient recursive board solving algorithm that is unlike other solutions I've
seen (I looked at examples online AFTER I finished writing the algorithm). It
implements a per-character depth-first search on a conservative tree. The game
also includes a simple GUI and a couple game states. The AI is extremely rudimentary
but I wanted to focus on making the interface smooth.

Construction:
- Poggle.pyw <- Run this file!
	This file contains the game singleton which manages events, initialization,
	and the game loop. The file also contains all classes directly dependent on
	GUI libraries. I have a lot to learn about GUI design patterns, but I tried
	to organize things in a coherent way. Everything can be accessed from the
	game object. More in-depth description of functionality can be read in the
	source.
- player.py, board.py, timer.py, die.py
	These files are model classes with no GUI dependency. They could theoret-
	ically be used to create an different version of the game with an entirely
	different interface.
- dicePickler.py, wordPickler.py
	These files are used to create serialized objects that are important to the
	functioning of Poggle, though they only need to run once to generate
	words.tree and dielist.list
- design directory:
	This directory contains all the design document and art source for the game
- resources directory:
	This directory contains all the images and fonts necessary to display the
	game

Current Status:
	As of right now, the game runs just fine. I would like to improve the oppo-
	nent AI at some point to make it more believable - for instance force it to
	usually pick 3 letter words over longer ones from the list. Right now it's 
	just as likely to pick a 16 letter word as it is a 3 letter one. Also, 
	there's a small non-fatal bug when quiting the application that causes 
	Tkinter to complain, but I think I need to learn more about GUIs to deal
	with it.

Requirements:
- Python 2.7 (32-bit required for PyGame)
- PyGame
