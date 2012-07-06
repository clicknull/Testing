# fummble -- general purpose fuzzer
# test_regfunchooks.py -- Test out printing registry keys from API calls in Advapi32.dll 
#

import pydbg
import os,sys
import utils

# gimmes: -Function-         -DLL- -ArgMap- -callback- -func name-
gimme=[]
gimme.append({'dll' : 'advapi32.dll', 'argmap': 'isddi', 'hook': 'hook_Reg', 'func' :'RegCreateKeyExA'})

pyd = pydbg.pydbg()
hooks = utils.hook_container()

# KISS for now... 
def hook_RegCreateKeyExA(pyd, args):
	buffer = ""
	offset = 0
	while 1:
		byte = pyd.read_process_memory(args[1]+offset, 1)
		if(byte != "\x00"):
			buffer += byte
			offset += 1
			continue
		else:
			break
	
	print "func(\""+buffer+"\")"
		

def hookme():
	hook_addrs = None
	hook_addr = pyd.func_resolve_debuggee(gimme[0]['dll'], gimme[0]['func'])
	if not hook_addr:
		print "[-] couldn't hook address of "+gimme[0]['func']+" in "+gimme[0]['dll']
		sys.exit(-1)
	print "[+] hooked "+gimme[0]['func']+"('"+gimme[0]['argmap']+"') in "+gimme[0]['dll'] + " at 0x%08x !" % hook_addr
	hooks.add(pyd, hook_addr, 9, hook_RegCreateKeyExA, None) # change me later..
	hook_addrs = hook_addr #later .append(
	return hook_addrs

def go():
	print "test_regfunchooks.py"
	
	for (pid, app) in pyd.enumerate_processes():
		print "%d:%s" % (pid,app)
		if(app.lower() == sys.argv[1]):
			print "\n[!] Target pid: "+str(pid)+" found."
			break
	try:
		pyd.attach(int(pid))
	except:
		if(app.lower() == sys.argv[1]):
			print "[-] could not attach to %d:%s" % (pid,app)
		else:
			print "[-] couldn't find " + str(sys.argv[1])
		sys.exit(-1)
	print "[+] Attached"
	hookme()
	pyd.run()

if __name__ == "__main__":
	go()
