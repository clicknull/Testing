# fummble -- general purpose fuzzer
# test_regfunchooks.py -- Test out printing registry keys from API calls in Advapi32.dll 
#

import pydbg
import os,sys
import utils

gimme=[]

HKEY_CLASSES_ROOT =		'0x80000000L'
HKEY_CURRENT_USER =		'0x80000001L'
HKEY_LOCAL_MACHINE =	'0x80000002L'
HKEY_USERS =			'0x80000003L'

hkeys={}
hkeys[HKEY_CLASSES_ROOT] = "HKEY_CLASSES_ROOT"
hkeys[HKEY_CURRENT_USER] = "HKEY_CURRENT_USER"
hkeys[HKEY_LOCAL_MACHINE] = "HKEY_LOCAL_MACHINE"
hkeys[HKEY_USERS] = "HKEY_USERS"

pyd = pydbg.pydbg()
hooks = utils.hook_container()

# KISS for now... 
def read_arg_str(pyd, args, arg_num):
	arg_num -= 1
	buffer = ""
	offset = 0

	if args == 0: # NULL case
		return 0
	while 1:
		byte = pyd.read_process_memory(args[arg_num]+offset, 1)
		if(byte != "\x00"):
			buffer += byte
			offset += 1
			continue
		else:
			break
	if(len(buffer) > 0):
		return buffer
	else:
		return -1


# 64 bit option? # for reading size values from pointers..
def read_arg_int(pyd, args, arg_num):
	arg_num -= 1
	the_int = int(pyd.read_process_memory(args[arg_num], 4))
	return the_int

# call backs
def hook_RegCreateKeyExA(pyd, args):
	buf=read_arg_str(pyd, args, 2)
	print "RegCreateKeyExA(\""+buf+"\")"

def hook_RegQueryValueExA(pyd, args):
	buf=read_arg_str(pyd, args, 2)
	print "RegQueryValueExA(\""+buf+"\")"

def hook_RegGetValueA(pyd, args):
	buf=read_arg_str(pyd, args, 2)
	print "RegGetValueA(\""+buf+"\")"

def hook_RegOpenKeyExA(pyd, args):
	buf=read_arg_str(pyd, args, 2)
	try:
		key=hkeys[hex(args[0])]
	except:
		key=str(hex(args[0]))
	print "RegOpenKeyExA("+key+", \""+buf+"\")"


def hookme():
	hook_addrs = []
	i=0
	for to_hook in gimme:
		if not to_hook['enabled']:
			continue
		hook_addr = pyd.func_resolve_debuggee(to_hook['dll'], to_hook['func'])
		if not hook_addr:
			print "[-] couldn't hook address of "+to_hook['func']+" in "+to_hook['dll']
			sys.exit(-1)
		print "[+] hooked "+to_hook['func']+"('"+to_hook['argmap']+"') in "+to_hook['dll'] + " at 0x%08x !" % hook_addr
		hooks.add(pyd, hook_addr, 9, to_hook['callback'], None) # change me later..
		hook_addrs.append(hook_addr)
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
	gimme.append({'enabled': True, 'dll' : 'advapi32.dll', 'argmap': 'isddi', 'callback': hook_RegCreateKeyExA, 'func' :'RegCreateKeyExA'})
	gimme.append({'enabled': True, 'dll' : 'advapi32.dll', 'argmap': 'isddi', 'callback': hook_RegQueryValueExA, 'func' :'RegQueryValueExA'})
	gimme.append({'enabled': True, 'dll' : 'advapi32.dll', 'argmap': 'isddi', 'callback': hook_RegOpenKeyExA, 'func' :'RegOpenKeyExA'})
	gimme.append({'enabled': True, 'dll' : 'advapi32.dll', 'argmap': 'isddi', 'callback': hook_RegOpenKeyExA, 'func' :'RegOpenKeyA'})
	go()