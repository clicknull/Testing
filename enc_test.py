# encryption test

from Crypto.Cipher import AES
import os
enc = AES.new(os.urandom(32), AES.MODE_CBC)
msg="123456789012"
print str(16-(msg.__len__() % 16))
if((msg.__len__() % 16) != 0):
    msg = msg + "\x00"*(16-msg.__len__() % 16) # spacing for pads?
print str(msg.__len__())
print msg
msg=enc.encrypt(msg)
print msg