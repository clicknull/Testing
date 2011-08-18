#!/usr/bin/python

#
# sc2cast.py -- Watches for certain players on sc2cast, if their stream goes online alert
# the user via xmessage
# edit towatch[] based on ur own prefs
# 

import urllib
import sgmllib
import time
import os

towatch=['Destiny', 'IdrA', 'Artosis'] # Case sensitive, look on site
site="http://sc2casts.com" 

def alert_on(player):  #maybe i'll do TK later if im up for it
	#if(os.fork() == 0):
		os.system("xmessage SC2CAST ALERT: " + player + " is on! &")

class Parse(sgmllib.SGMLParser):
	def parse(self, s):
		self.feed(s)
		self.close()
	def __init__(self, verbose=0):
		sgmllib.SGMLParser.__init__(self,verbose)
		self.online_streams = []
	def start_a(self, attr):
		for name, val in attr:
			if name == "href":
				self.online_streams.append(site + val)
	def gimme(self):
		return self.online_streams 

while(1):
	time.sleep(1)
	fd=urllib.urlopen(site)
	html=fd.read()
	fd.close()
	online = r"<span style='color:green'>Online</span>"
	offset=html.find(online)+online.__len__()
	endset=html[offset:].find("span")
	if(endset == -1): #weird error i get 90% of the time is urlopen returns a garbage fd :|
		continue
	html=html[offset:offset+endset]
	p=Parse()
	p.parse(html)

	print "Online:"
	for url in p.gimme():
		print url
		for w in towatch:
			if(url.find(w) != -1):
				alert_on(w)

