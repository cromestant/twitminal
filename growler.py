from Growl import *


class growler(GrowlNotifier): 
	def __init__(self): 
		self.applicationName = 'Twitminal' 
		self.applicationIcon = Image.imageWithIconForApplication('/Applications/Utilities/Console.app') 
		self.notifications = ['Twitminal msg'] 
		self.register() 

