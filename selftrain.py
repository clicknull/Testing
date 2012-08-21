# Self Trainer:
# -denies access to a list of applications (mostly games I guess) and records
# - maybe later monitors for long bouts of inactive keyboard usage?

import pydbg
import os
from pydbg.defines import *
import time

# list of programs to monitor for/kill
program_list = ["sc2.exe", "iw5mp.exe", "smplayer.exe"]

pydb = pydbg.pydbg()

if __name__ == "__main__":
	while(1):
		time.sleep(10)
		for (pid, app) in pydb.enumerate_processes():
			for nono in program_list:
				if(nono.lower() == app.lower()):
					print "Logged an attempt at running: (%s:%d)" % (app,pid)
					os.system("taskkill /F /im "+app)
				else:
					pass