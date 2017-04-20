#	___ _ _  _ ____ ____ 
#	 |  | |\/| |___ |__/ 
#	 |  | |  | |___ |  \ .py
#	                     
# This class defines a model countdown timer with start, pause, reset,
# and output functionality.

from time import *

class Timer:
	'''A countdown timer'''
	def __init__(self, length, callback=lambda: None): # length is in msecs
		'''Init the timer with (timer length, callback = optional callback function)'''
		self.length = length
		self.pauseStartTime = 0
		self.pauseLength = 0
		self.lastTime = 0
		self.startTime = time()*1000 # time() returns seconds so time() must be multiplied by 1000 to yield mSecs
		self.paused = False # necessary to allow timer to pause itself initially
		self.pause()
		self.callback = callback

	def start(self):
		self.resume() #identical fncs

	def reset(self, length=None, callback=None): # resets the timer, giving the user an opportunity to reset its settings
		'''Resets the timer to its original length and callback function unless they're passed as named params'''
		if length == None:
			length = self.length
		if callback == None:
			callback = self.callback
		self.__init__(length, callback)

	def msecsLeft(self):
		'''Returns milliseconds left till the timer is finished'''
		if self.paused:
			return self.lastTime
		now = self.length - (time() * 1000 - self.startTime - self.pauseLength) # Current time is equal to 
		# the initial timer length plus the startTime plus the length of pauses minus the current time
		if now < 0: # don't let the timer run past 0
			return 0
		else:
			return now

	def minSecsLeft(self):
		'''Returns the time left like this "2:34"'''
		now = self.msecsLeft()
		return "%01i:%02i" % (now/(60000)%60, now/1000%60)

	def pause(self):
		if not self.paused: # if it's not already paused
			self.pauseStartTime = time()*1000 #set a mini timer starting right now
			self.lastTime = self.msecsLeft() #the time at which the timer was paused. This is done
			# so that if msecsLeft() is called while the timer is paused, it can give a coherent answer
			self.paused = True

	def resume(self):
		if self.paused:
			#add the time during most recent pause to all the pause length
			self.pauseLength += time()*1000 - self.pauseStartTime
			self.paused = False

	def update(self):
		'''Update the timer - should be called during main loop to check if the time has run out'''
		currTime = self.minSecsLeft()
		if self.msecsLeft() <= 0: #if the timer is done, do the callback function and pause.
			self.callback()
			self.pause()
		return currTime