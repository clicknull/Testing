#/usr/bin/python

#
# PTSniff - basic /proc/[pid]/fd/* sniffage.
#


import os
import sys

if(len(sys.argv) < 2):
	print "Usage: ./PTSniff.py <pid>"
	sys.exit(1)
path = "/proc/%d/fd" % int(sys.argv[1])
fds = os.listdir(path)
if(not fds):
    print "there are no sockets to be found here!"
to_read = []
for fd in fds:
    maybe_read = os.readlink(path+ "/" + fd)
    if(not maybe_read in to_read):
	to_read.append(maybe_read)
	   
print "Pick an FD to sniff:"
i=0
for fd in to_read:
    print "["+str(i)+"] "+ fd
    i+=1
choice=int(raw_input())
print "starting line-read from: " + to_read[choice]
reading=open(to_read[choice], "r")
writing=open(to_read[choice], "w")
#try:
if(True):
    while(1):
	byte = reading.read(5)
	#writing.write(byte)
	sys.stdout.write(byte)

#except:
#    print "zomg it failed reading from the fd"
	

