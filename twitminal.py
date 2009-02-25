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


def printHelpMenu():
	print "Twitminal- by Charz"
	print "--help menu:"
	print "--Available commands :"
	print "  --help (prints this menu)"
	print "  --last (shows last non-empty import of twits)"
	print "  --direct:<name>:<message> (posts direct message to user)"
	print "  --friendsList (prints friends list)"
	print "  exit() (Kills notifier thread, then quits)"

def handler(signum, frame):
	print "Killing thread"
	mychecker.stopNdone()
	while mychecker.isAlive():
		print "Thread still alive, wait a tick!"
		sleep(3)
	print "Bye bye"
	sys.exit()

print reset,"Welcome! Twitminal, minimal twitter client with growl notifications!\nBy Charz! (Charles Romestant)"
print "cromestant@gmail.com\n\n"
print "Twitter username: "
username = sys.stdin.readline()[:-1]
print "Twitter Password: "
password=sys.stdin.readline()[:-1]

try:
	api=twitter.Api(username,password,'utf-8')
	friends = api.GetFriends()
except:
	print "Authorization error\nor comunication errors"
	sys.exit()
print "Type 'quit()' to exit --help for commands\nAnything else WILL be twitted!\n"
signal.signal(signal.SIGINT, handler)
mychecker = checker.checker(username,password)
mychecker.start()
loop= True
while loop:
	print "Twitminal : #"
	text = sys.stdin.readline()[:-1]
	if text=='quit()' or text=='exit()':
		mychecker.stopNdone()
		loop =False
		while mychecker.isAlive():
			print "Thread still alive, wait a tick!"
			sleep(3)
		print "Bye bye"
	elif text.startswith("--help"):
		printHelpMenu()
	elif text.startswith("--last"):
		lastl = mychecker.getLastLine()
		for f in lastl:
			print f.GetUser().screen_name+": "+f.GetText()
	elif text.startswith("--direct:"):
		x= text.partition(":")[2].partition(":")
		if len(x[2])<141:
			api.PostDirectMessage(x[0],x[2])
	elif text=="--friendsList":
		friends = api.GetFriends(username)
		for f in friends:
			print f.screen_name
	elif len(text)>140:
		print "over 140 characters.."
	else:
		#send twitt!
		api.PostUpdate(text)
		
