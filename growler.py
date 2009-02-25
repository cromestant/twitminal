from Growl import *


class growler(GrowlNotifier): 
	def __init__(self): 
		self.applicationName = 'Twitminal' 
		self.applicationIcon = Image.imageWithIconForApplication('/Applications/Utilities/Console.app') 
		self.notifications = ['Twitminal msg'] 
		self.notify(self.notifications[0],'Twitminal','estarteando esta verga!\n')
		self.register()
	def send(self,app,who,what):
		self.notify(self.notifications[0],app,who+": "+what)

