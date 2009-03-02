import sys
import os
import datetime
import twitter
from time import localtime,asctime,sleep
import threading
import growler

class checker ( threading.Thread ):
	last=""
	lastLine=None
	growl=None
	ndone = True
	username=""
	password=""
	api=None
	i=0
	def __init__(self,username,password):
		self.notifiers=[]
		growl = growler.growler()
		self.notifiers.append(growl)
		self.username = username
		self.password=password
		self.log =False
		self.api = twitter.Api(self.username,self.password)
		self.api.SetXTwitterHeaders('Twitminal','none-yet', 'V.0.1')
		threading.Thread.__init__(self)
	def run ( self ):
		while self.ndone:
			try:
				if(self.i==0):
					friendsline = self.api.GetFriendsTimeline(user=self.username,since=self.last)
					if len(friendsline)>0:
						self.setLastLine(friendsline)
					d= datetime.datetime.now()
					self.last = d.strftime("%a, %d %b %Y %H:%M:%S -0430")
					temp=""
					for f in friendsline:
						for n in self.notifiers:
							n.send('Twitminal',f.GetUser().screen_name,f.GetText())
						#temp+=f.GetUser().screen_name+": "+f.GetText()+"\n"
					#self.growl.notify(self.growl.notifications[0],'Twitminal',temp)
				self.i=(self.i+1)%18
				sleep(10)
			except:
				print "error",sys.exc_info()[0]
				raise
	def stopNdone(self):
		self.ndone=False
		print "about to kill checker thread\n"
	def setLastLine(self,newline):
		lock =threading.Lock()
		lock.acquire()
		if self.log:
			self.lastLine.extend(newline)
		else:
			self.lastLine = newline
		lock.release()
	def getLastLine(self):
		return self.lastLine
	def logTweets(self):
		"""sets log flag to log"""
		self.log = not self.log
		return self.log
	def clearLog(self):
		"""Clears log"""
		self.lastLine =[]