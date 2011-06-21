#!/usr/bin/python
import thread as _thread, time

mutex=_thread.allocate_lock()

def count(_id,num):
	
	while (num < 10):
		mutex.acquire()
		num += 1
		print str(_id) + ": " + str(num)
		mutex.release()
		time.sleep(1)
if(__name__ == "__main__"):
	global num
	num = 0	
	mutex=_thread.allocate_lock()
	for i in range (5):
		_thread.start_new_thread(count, (i,num))
	time.sleep(5) # not using join() just waiting for the other threads
	print "main thread exiting..."
