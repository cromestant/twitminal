import sys
import os
import datetime
import twitter
import checker
import signal
import chardet
from time import localtime,asctime,sleep

username=''
password=''
mychecker=None
esc = '%s['%chr(27)
reset = '%s0m'%esc
red ='%s31m'%esc
blue ='%s36m'%esc
green ='%s32m'%esc

def printc(color,text):
	print color,text,reset
	
def printHelpMenu():
	printc(reset,"Twitminal- by Charz")
	printc (green,"--help menu:")
	printc (green,"--Available commands :")
	printc (green,"  --help (printcs this menu)")
	printc (green,"  --last (shows last non-empty import of twits)")
	printc (green,"  --direct:<name>:<message> (posts direct message to user)")
	printc (green,"  --friendsList (printcs friends list)")
	printc (green,"  exit() (Kills notifier thread, then quits)")

def handler(signum, frame):
	printc (red,"Killing thread")
	mychecker.stopNdone()
	while mychecker.isAlive():
		printc (red,"Thread still alive, wait a tick!")
		sleep(3)
	printc (reset,"Bye bye")
	sys.exit()

print("Welcome! Twitminal, minimal twitter client with growl notifications!\nBy Charz! (Charles Romestant)")
printc (blue,"cromestant@gmail.com\n\n")
print("Twitter username: ")
username = sys.stdin.readline()[:-1]
print("Twitter Password: ")
password=sys.stdin.readline()[:-1]

try:
	api=twitter.Api(username,password,'utf-8')
	friends = api.GetFriends()
except:
	printc (red,"Authorization error\nor comunication errors")
	sys.exit()
printc (green,"Type 'quit()' to exit --help for commands\nAnything else WILL be twitted!\n")
signal.signal(signal.SIGINT, handler)
mychecker = checker.checker(username,password)
mychecker.start()
loop= True
while loop:
	print("Twitminal : #")
	text = sys.stdin.readline()[:-1]
	if text=='quit()' or text=='exit()':
		mychecker.stopNdone()
		loop =False
		while mychecker.isAlive():
			printc (red,"Thread still alive, wait a tick!")
			sleep(3)
		print("Bye bye")
	elif text.startswith("--help"):
		printHelpMenu()
	elif text.startswith("--last"):
		lastl = mychecker.getLastLine()
		for f in lastl:
			printc (blue,f.GetUser().screen_name+": "+reset+f.GetText())
	elif text.startswith("--direct:"):
		x= text.partition(":")[2].partition(":")
		if len(x[2])<141:
			api.PostDirectMessage(x[0],x[2])
	elif text=="--friendsList":
		friends = api.GetFriends(username)
		for f in friends:
			printc(blue, f.screen_name)
	elif len(text)>140:
		printc (red,"over 140 characters..")
	else:
		#send twitt!
		api.PostUpdate(text)
		
