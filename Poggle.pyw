#	___  ____ ____ ____ _    ____ 
#	|__] |  | | __ | __ |    |___ 
#	|    |__| |__] |__] |___ |___ .py
#	                              
# This is the main program file. It contains the main game loop,
# controller objects that inherit the model classes stored in other
# files, a couple graphics objects, and a rudimentary events system.

#   _ _  _ ___  ____ ____ ___ ____ 
#   | |\/| |__] |  | |__/  |  [__  
#   | |  | |    |__| |  \  |  ___] 
#                                  
import Tkinter as tk
import pygame as pyg
import cPickle as pickle
import os, string, random, timer
from board import Board
from player import Player

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

#   ____ ____ _  _ ____    ____ _    ____ ____ ____ 
#   | __ |__| |\/| |___    |    |    |__| [__  [__  
#   |__] |  | |  | |___    |___ |___ |  | ___] ___] 
#                                                   
class Poggle():
	'''This is the main game class. Manages objects and events'''
	def __init__(self, dieList, wordTree, difficulty, gameLength):
		'''This is the main init of the entire game. Not meant to be polymorphic in any way'''

		pyg.font.init() # initialize font portion of pygame to load fonts

		self.status = 'welcome' # make a variable to hold current state. Set it to "Welcome" initially

		self.root = tk.Tk() # make a root window
		self.root.configure(background='#bf996b') # set the root window to be brown

		## BOARD LOADING SECTION ##
		# load the board's BG file
		boardBG = pyg.image.load('resources/images/background.png')
		
		#load dice images into a dictionary to pass to board obj
		diceImgs = {}
		i = 0
		for char in string.ascii_lowercase:
			if char == 'q':
				char = 'qu'
			diceImgs[char] = pyg.image.load('resources/images/dice/'+char+'.png')
		self.board = GraphicBoard(dieList,wordTree,boardBG,diceImgs)


		## TIMER LOADING SECTION ##
		#load the timer font
		self.lcdFont = pyg.font.Font("resources/fonts/lcd.ttf",30)
		self.timer = GraphicTimer(gameLength, self, self.lcdFont, self.outOfTime)

		## MESSAGER LOADING SECTION ##
		# Associate gamestates with message images
		messages = {
			'welcome' : pyg.image.load('resources/images/message_welcome.png'),
			'paused' : pyg.image.load('resources/images/message_paused.png'),
			'humanWon' : pyg.image.load('resources/images/message_won.png'),
			'opponentWon' : pyg.image.load('resources/images/message_lost.png'),
			'tied' : pyg.image.load('resources/images/message_tied.png')
		}
		self.messager = Messager(messages, (36,215))


		## RESET BUTTON LOADING SECTION ##
		# Create a set of images with which to draw the reset button
		resetImgs = [
			pyg.image.load('resources/images/buttons/reset_u.png'),
			pyg.image.load('resources/images/buttons/reset_h.png'),
			pyg.image.load('resources/images/buttons/reset_d.png')
		]
		self.resetButton = GraphicButton(resetImgs, (240,119), callback = self.reset) # init with a reset event callback


		## PAUSE TOGGLE BUTTON LOADING SECTION ##
		# Create two sets of images with which to draw the pause
		# toggle button: one for the pause command, and one for the
		# play command.
		pauseImgs = [
			pyg.image.load('resources/images/buttons/pause_u.png'),
			pyg.image.load('resources/images/buttons/pause_h.png'),
			pyg.image.load('resources/images/buttons/pause_d.png')
		]
		playImgs = [
			pyg.image.load('resources/images/buttons/play_u.png'),
			pyg.image.load('resources/images/buttons/play_h.png'),
			pyg.image.load('resources/images/buttons/play_d.png')
		]
		# init the button with a resume and pause event callback
		self.pauseToggleButton = GraphicToggleButton(playImgs, pauseImgs, (53,119), \
			callback1 = self.resume, callback2 = self.pause)

		# A little overboard, but make a list to hold the buttons. If I were to at some point turn the dice into buttons
		# as well, then they would be added to this list as well. It is used to deal with mouse down and up events.
		self.buttons = [self.pauseToggleButton,self.resetButton]

		## STATIC GUI ELEMENT INIT SECTION ##
		# Add a label to the human side
		tk.Label(self.root, text="You").grid(row = 0, column = 3, columnspan=2)
		self.human = HumanPlayer(self.root, self.board)
		# Add a label to the Dr. Evil side
		tk.Label(self.root, text="Dr. Evil").grid(row = 0, column = 0, columnspan=2)
		self.opponent = OpponentPlayer(difficulty, self.root, self.board)

		# Define the width of pygame frame
		gFrameWidth, gFrameHeight = 342, 535
		 
		# Add a couple widgets. Pygameframe will be in `gFrame`.

		self.gFrame = tk.Frame(self.root, width=gFrameWidth, height=gFrameHeight)
		self.gFrame.grid(row = 0, column = 2, rowspan = 4)

		# Tell pygame's SDL window which window ID to use. This puts PyGame's window inside the Tkinter GUI
		# From http://stackoverflow.com/questions/8584272/using-pygame-features-in-tkinter
		os.environ['SDL_WINDOWID'] = str(self.gFrame.winfo_id())

		# Show the window so it's assigned an ID.
		self.root.update()

		# Usual pygame initialization
		pyg.display.init()
		self.gScreen = pyg.display.set_mode((gFrameWidth,gFrameHeight), pyg.DOUBLEBUF, 32)

	def begin(self):
		self.resetButton.disable() # Disable the resetButton during the welcome screen
		self.run() # enter main game loop

#   _  _ ____ _ _  _    _    ____ ____ ___  
#   |\/| |__| | |\ |    |    |  | |  | |__] 
#   |  | |  | | | \|    |___ |__| |__| |    
#                                           
	def run(self):
		while True: # infinite loop
			#Look at the event stack
			for event in pyg.event.get():
				if event.type == pyg.QUIT: # If the game has been quit, exit.
					pyg.quit()
					sys.exit()
				elif event.type == pyg.MOUSEBUTTONDOWN: 
					if event.button == 1:
						for button in self.buttons:
							button.mouseChange("DOWN")
				elif event.type == pyg.MOUSEBUTTONUP:
					if event.button == 1:
						for button in self.buttons:
							button.mouseChange("UP")

			state = self.status
			if state == 'welcome':
				self.board.update(self.gScreen)
				self.timer.update(self.gScreen)
				self.pauseToggleButton.update(self.gScreen)
				self.messager.displayMessage(self.gScreen,state)

			if state == 'running':
				self.board.update(self.gScreen)
				self.board.updateDice(self.gScreen)
				self.human.update()
				self.opponent.update()
				self.timer.update(self.gScreen)
				self.resetButton.update(self.gScreen)
				self.pauseToggleButton.update(self.gScreen)
				
			elif state == 'paused':
				self.board.update(self.gScreen)
				self.timer.update(self.gScreen)
				self.resetButton.update(self.gScreen)
				self.pauseToggleButton.update(self.gScreen)
				self.messager.displayMessage(self.gScreen,state)
				
			#the loops are identical for all endgame states
			elif state == 'opponentWon' or state == 'humanWon' or state == 'tied':
				self.board.update(self.gScreen)
				self.board.updateDice(self.gScreen)
				self.messager.displayMessage(self.gScreen,state)
				self.resetButton.update(self.gScreen)

			# Update the pygame display
			pyg.display.flip()

			self.root.update() #Not sure about how to handle the "Application has been destroyed" error

	#Event Functions:
	def pause(self):
		self.status = 'paused'
		self.timer.pause()
		self.human.pause()

	def resume(self):
		self.status = 'running'
		self.timer.resume()
		self.human.resume()
		self.resetButton.enable()

	def reset(self):
		self.timer.reset()
		self.human.reset()
		# if reset it called after the game ends, reset the game and start it automatically
		if self.status != 'running' and self.status != 'paused' and self.status != 'welcome':
			self.human.eraseOutputScore()
			self.opponent.eraseOutputScore()
			self.status = 'running'
			self.timer.start()
			self.pauseToggleButton.setState(1)
		else: #Otherwise, reset but don't start automatically
			self.status = 'paused'
			self.pauseToggleButton.setState(0)
			self.human.pause()
		#either way, shake the board and enable stuff
		self.board.shake()
		self.pauseToggleButton.enable()
		self.opponent.reset()

	def outOfTime(self):
		#Calculate scores
		humanScore = self.human.calcScore()
		opponentScore = self.opponent.calcScore()
		# Depending on the outcome, go to three different states
		if humanScore > opponentScore:
			self.status = 'humanWon'
		elif opponentScore > humanScore:
			self.status = 'opponentWon'
		else: #tie
			self.status = 'tied'
		self.opponent.revealWords()
		self.opponent.outputScore()
		self.human.pause()
		self.human.outputScore()
		self.pauseToggleButton.disable()


#   _  _ _  _ _  _ ____ _  _ ___  _    ____ _   _ ____ ____ 
#   |__| |  | |\/| |__| |\ | |__] |    |__|  \_/  |___ |__/ 
#   |  | |__| |  | |  | | \| |    |___ |  |   |   |___ |  \ 
#                                                           
class HumanPlayer(Player):
	'''A child of the player class, HumanPlayer includes GUI specific functions to support input, etc'''
	def __init__(self, root, board):
		'''Init the object. Requires the root window for GUI init and the board for checking words'''
		self.root = root
		self.board = board
		self.entryV = tk.StringVar()
		self.wordListBox = tk.Text(width=20,height=20)
		self.wordListBox.grid(row = 2, column = 3, columnspan = 2) # place to the right of the pygame window
		Player.__init__(self) # run the parent init
	def update(self):
		'''Rewrites the entry field with capitalized version of the word'''
		self.entryV.set(self.entryV.get().upper())#make entry into user field always capitalized every frame
	def outputScore(self):
		'''This is run at the end of a game - it outputs the human's score to the GUI'''
		self.scoreWidget = tk.Label(self.root, text="Score: "+str(self.score))
		self.scoreWidget.grid(row = 3, column = 3, columnspan=2) # lower right corner
	def eraseOutputScore(self):
		'''The is called on a new game. It removes the GUI score element from last game'''
		self.scoreWidget.destroy()
	def checkWord(self,stringObj):
		'''This checks a string against the board's list of words'''
		word = stringObj.get() # get the string from the passed string object
		self.addWord(word, self.board.getSolvedWords()) # a superclass fnc - adds the word if its in the "OK" list
		stringObj.set('') # reset the input field
		#write the updated list of player's good words to the GUI
		self.wordListBox.config(state=tk.NORMAL)
		self.wordListBox.delete(1.0, tk.END)
		self.wordListBox.insert(tk.END, self.outputWords())
		self.wordListBox.config(state=tk.DISABLED)
	def reset(self):
		'''This reset function is called on a new game. It erases the player's previous words and
		removes some GUI elements'''
		#remove old entry and button widgets
		self.entry.destroy()
		self.entryButton.destroy()

		#create new entry and button widgets
		self.entryV = tk.StringVar()
		self.entryV.set('')
		self.entry = tk.Entry(self.root, textvariable=self.entryV)
		self.entry.grid(row = 1, column = 3)

		self.entry.bind('<Return>', lambda event: self.checkWord(self.entryV))
		self.entryButton = tk.Button(self.root, text="enter", command = lambda: self.checkWord(self.entryV))#self.checkWord(word = self.entryV.get()))
		self.entryButton.grid(row = 1, column = 4)
		self.wordListBox.config(state=tk.NORMAL)
		self.wordListBox.delete(1.0, tk.END)
		self.wordListBox.config(state=tk.DISABLED)
		Player.reset(self)
	def pause(self):
		'''Removes the GUI widgets to prevent the user from trying to enter words while the game is paused'''
		self.entryV.set('')
		self.entryButton.destroy()
		self.entry.destroy()
	def resume(self):
		'''Adds the GUI widgets back'''
		self.entryV = tk.StringVar()
		self.entryV.set('')
		self.entry = tk.Entry(self.root, textvariable=self.entryV)
		self.entry.grid(row = 1, column = 3)
		self.entry.bind('<Return>', lambda event: self.checkWord(self.entryV))
		self.entryButton = tk.Button(self.root, text="enter", command = lambda: self.checkWord(self.entryV))#self.checkWord(word = self.entryV.get()))
		self.entryButton.grid(row = 1, column = 4)

class OpponentPlayer(Player):
	'''A child of the player class, OpponentPlayer adds a simple GUI and a rudimentary AI'''
	def __init__(self, difficulty, root, board): # difficulty from 0 to 10
		'''Init the object'''
		self.difficulty = difficulty
		self.root = root
		self.board = board
		self.wordListBox = tk.Text(width=18,height=20)
		self.wordListBox.grid(row = 2, column = 0, columnspan = 2) #Place to the left of the PyGame window
		Player.__init__(self)
	def update(self):
		'''Adds a word to its list every so often'''
		# Every 1000*difficulty or so frames, the the opponent adds a word to its word list
		if random.random()*1000 < self.difficulty:
			solvedWords = self.board.getSolvedWords()
			self.addWord(solvedWords[random.randrange(len(solvedWords))], solvedWords)
			self.wordListBox.config(state=tk.NORMAL)
			self.wordListBox.delete(1.0, tk.END)
			self.wordListBox.insert(tk.END, self.outputHiddenWords())
			self.wordListBox.config(state=tk.DISABLED)
	def outputHiddenWords(self):
		'''This function does the same as outputWords() but replaces all chars with Xs
		to make the human player more interested. Or something.'''
		words = ""
		for word in self.foundWords:
			words += len(word)*'X' +"\n"
		return words
	def outputScore(self):
		'''Build a widget to show the score'''
		self.scoreWidget = tk.Label(self.root, text="Score: "+str(self.score))
		self.scoreWidget.grid(row = 3, column = 0, columnspan=2)
	def eraseOutputScore(self):
		'''Remove score widget'''
		self.scoreWidget.destroy()
	def reset(self):
		'''Erase the word list box and reset'''
		self.wordListBox.config(state=tk.NORMAL)
		self.wordListBox.delete(1.0, tk.END)
		self.wordListBox.config(state=tk.DISABLED)
		Player.reset(self)
	def revealWords(self):
		'''the normal reveal outputWords function'''
		self.wordListBox.config(state=tk.NORMAL)
		self.wordListBox.delete(1.0, tk.END)
		self.wordListBox.insert(tk.END, self.outputWords())
		self.wordListBox.config(state=tk.DISABLED)


#   ____ ____ ____ ___  _  _ _ ____ ____ ___  ____ ____ ____ ___  
#   | __ |__/ |__| |__] |__| | |    [__  |__] |  | |__| |__/ |  \ 
#   |__] |  \ |  | |    |  | | |___ ___] |__] |__| |  | |  \ |__/ 
#                                                                 
class GraphicBoard(Board):
	'''a simple graphics wrapper around the Board class'''
	def __init__(self, dieList, wordTree, bgImage, diceImgs):
		'''Inits the class, taking background and dice images'''
		self.bgImage = bgImage
		self.diceImgs = diceImgs
		Board.__init__(self,dieList,wordTree)
	def update(self,screen):
		'''display the background'''
		screen.blit(self.bgImage,(0,0))
	def updateDice(self,screen):
		'''Display the dice on the board'''
		for j in range(self.size):
			for i in range(self.size):
				screen.blit(self.diceImgs[self.getDieVal((i,j)).lower()],(i*65+44,j*68+222))

#   ___ _ _  _ ____ ____    ____ _    ____ ____ ____ 
#    |  | |\/| |___ |__/    |    |    |__| [__  [__  
#    |  | |  | |___ |  \    |___ |___ |  | ___] ___] 
#                                                    
class GraphicTimer():
	'''A simple graphic timer. Composes rather than inherits the Timer class'''
	def __init__(self, length, game, font, callback = lambda: None):
		self.game = game
		self.font = font
		self.timer = timer.Timer(length, callback)
	def update(self, screen):
		timeStr = self.timer.update()
		surface = self.font.render(timeStr, True, (0,231,0), (161,130,92))
		screen.blit(surface, (137,128))#draw timeStr on the surface
	def pause(self):
		self.timer.pause()
	def resume(self):
		self.timer.resume()
	def start(self):
		self.timer.start()
	def reset(self):
		self.timer.reset()

#   ___  _  _ ___ ___ ____ _  _    ____ _    ____ ____ ____ ____ ____ 
#   |__] |  |  |   |  |  | |\ |    |    |    |__| [__  [__  |___ [__  
#   |__] |__|  |   |  |__| | \|    |___ |___ |  | ___] ___] |___ ___] 
#                                                                     

class GraphicButton():
	'''A simple graphic button class with three images and one state. Can be hovered and clicked.'''
	def __init__(self, buttonSet, pos, callback = lambda: None):
		'''Init the button. ButtonSet is a list like this [upImage,hoverImage,downImage]'''
		self.buttonSet = buttonSet
		self.callback = callback
		self.pos = pos
		self.surface = self.buttonSet[0]
		self.down = False
		self.disabled = False
	def mouseChange(self,nowState):
		'''Gets mouse event from PyGame event stack and updates itself accordingly.
		This extra complexity prevents the callback function from being called every
		frame while the button is being clicked'''
		if self.inside(pyg.mouse.get_pos()) and self.disabled == False:
			if nowState == "DOWN":
				self.down = True
				self.callback()
			elif nowState == "UP":
				self.down = False
	def update(self, screen):
		'''Checks the button's hover and down positions and displays accordingly'''
		if self.disabled == False: 
			if self.inside(pyg.mouse.get_pos()): #If mouse is hovering
				if self.down: # if mouse is clicked
					surface = self.buttonSet[2] # set the image to be down and hovered
				else:
					surface = self.buttonSet[1] # set the image to be hovered
			else:
				surface = self.buttonSet[0] # set the image to be normal
			# as long as the button is enabled, draw it on the screen
			screen.blit(surface, self.pos)
	def disable(self):
		'''Disable the button'''
		self.disabled = True
	def enable(self):
		'''Enable the button'''
		self.disabled = False
	def inside(self, testPt):
		'''A simple rectangle test to check whether the mouse is over the button - returns bool'''
		if testPt[0] >= self.pos[0] and testPt[0] <= (self.pos[0] + self.surface.get_size()[0]) \
		and testPt[1] >= self.pos[1] and testPt[1] <= (self.pos[1] + self.surface.get_size()[1]): #first line checks x, second, y
			return True
		else:
			return False

class GraphicToggleButton(GraphicButton):
	'''Inherits GraphicButton and adds support for two button sets and toggling between them'''
	def __init__(self, buttonSet1, buttonSet2, pos, callback1 = lambda: None, callback2 = lambda: None):
		'''Init and take two button sets and two callback functions'''
		self.buttonSetList = [buttonSet1, buttonSet2]
		self.callbackSet = [callback1, callback2]
		self.state = 0
		self.buttonSet = self.buttonSetList[self.state]
		self.callback = self.callbackSet[self.state]
		self.pos = pos
		GraphicButton.__init__(self, self.buttonSet, self.pos, callback = self.toggle)
	def update(self, screen):
		'''Draw the button'''
		self.buttonSet = self.buttonSetList[self.state] # set the variable the 
		# superclass uses for picking images to be whatever buttonset corresponds
		# to the current button class
		GraphicButton.update(self, screen)
	def toggle(self):
		'''Toggles the button's state'''
		self.callbackSet[self.state]()
		self.state = int(not bool(self.state)) # toggles self.state between 0 and 1
	def setState(self,newState):
		'''Manually over-rides the button's current state'''
		self.state = newState

#   _  _ ____ ____ ____ ____ ____ ____ 
#   |\/| |___ [__  [__  |__| | __ |___ 
#   |  | |___ ___] ___] |  | |__] |___ 
#                                      
class Messager():
	'''A simple class for displaying messages over the Poggle board'''
	def __init__(self,messageDict, pos):
		'''Takes pygame images as a dict'''
		self.messageDict = messageDict
		self.pos = pos
	def displayMessage(self,screen,message):
		'''Draws the message on the screen'''
		screen.blit(self.messageDict[message],self.pos)

#Run the program!
theGame = Poggle(dieList,wordTree,3,180000)#Difficulty of 3, 18000 milliseconds (3 mins) long
theGame.begin()