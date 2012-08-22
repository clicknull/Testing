# Self Trainer:
# -denies access to a list of applications (mostly games I guess) and records
# - maybe later monitors for long bouts of inactive keyboard usage?

import pydbg
import os
from pydbg.defines import *
import time

import win32api
import win32process
import win32gui

# list of programs to monitor for/kill
deny_program_list = ["sc2.exe", "iw5mp.exe", "smplayer.exe"]

# list of window titles to monitor for/kill
deny_title_list = ["slashdot", "reddit", "facebook"]

pydb = pydbg.pydbg()
w=win32gui

if __name__ == "__main__":
	while(1):
		time.sleep(1)
		# check the process list
		for (pid, app) in pydb.enumerate_processes():
			for nono in deny_program_list:
				if(nono.lower() == app.lower()):
					print "Logged an attempt at running: (%s:%d)" % (app,pid)
					os.system("taskkill /F /im " + app)
				else:
					pass
		#check the window title of current window
		window_text = w.GetWindowText(w.GetForegroundWindow())
		pid=str(win32process.GetWindowThreadProcessId(w.GetForegroundWindow())[1])
		for nono in deny_title_list:
			# perhaps better to match exactly here?
			if(nono.lower() in window_text.lower()):
				print "Logged an attempt of a window containing %s: (%s:%s)" % (nono, window_text, pid)
				os.system("taskkill /PID " + pid)
