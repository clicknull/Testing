#!/usr/bin/python

#
# sc2cast.py -- Watches for certain players on sc2cast, if their stream goes online alert
# the user via xmessage
# edit towatch[] based on ur own prefs
# 

import urllib
import sgmllib
import time
import os, sys
import threading

class sc2cast(threading.Thread):
	def __init__(self):
		self.towatch = ['Destiny', 'IdrA', 'Artosis'] # Case sensitive, look on self.site
		self.site = "http://sc2casts.com" 
		threading.Thread.__init__(self)
	
	def alert_on(player):  # this will later have its own class.. for bot plugin
		#if(os.fork() == 0):
			os.system("xmessage SC2CAST ALERT: " + player + " is on! &")
	
	class Parse(sgmllib.SGMLParser):
		def parse(self, s):
			self.feed(s)
			self.close()
		def __init__(self, verbose=0):
			sgmllib.SGMLParser.__init__(self, verbose)
			self.online_streams = []
		def start_a(self, attr):
			for name, val in attr:
				if name == "href":
					self.online_streams.append(val)
		def gimme(self):
			return self.online_streams 
	
	def run(self):
		while(1):
			time.sleep(1)
			try:
				fd = urllib.urlopen(self.site)
			except:
				print "URLopen failed"
				continue
			
			html = fd.read()
			fd.close()
			online = r"<span style='color:green'>Online</span>"
			offset = html.find(online) + online.__len__()
			endset = html[offset:].find("span")
			if(endset == -1): #weird error i get 90% of the time is urlopen returns a garbage fd :|
				continue
			html = html[offset:offset + endset]
			p = sc2cast.Parse()
			p.parse(html)
		
			print "Online:"
			for url in p.gimme():  #sloppy, do something else
				print self.site+url
				for w in self.towatch:
					if(url.find(w) != -1):
						self.alert_on(self.site+w)
try:
	sc=sc2cast()
	sc.start()
	while(1):  #take this out when plugin is completed
		time.sleep(1)
except KeyboardInterrupt:
	print "caught ctrl+c"
	sys.exit(1)