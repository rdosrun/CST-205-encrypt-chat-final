# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import math
import encrypt_header
import time
import json
from PyQt5.QtCore import QThread

key = 0;
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
name=input("please enter your username:")
sys.argv.append('127.0.0.1')#"192.168.43.101")
sys.argv.append(25565)
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number")
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))
self_ob = encrypt_header.client(name,(IP_address,Port))

#handshake
message = server.recv(2048)
message = message.decode("utf-8")
if("time_seed:" == message[0:10]):
	x = [int(s) for s in message.split() if s.isdigit()]
	tmp_seed = x[0]
	print(tmp_seed)
	key = self_ob.key_gen(tmp_seed)
	print("key:",key)
	pub = self_ob.diff_hullman_ex_gen(key)
	print("pub:",pub)
	server.send(str(pub).encode())
	print("Welcome to this chatroom!") 
server.send(name.encode())

#end handshake

def con_2_person(name):
	server.send(("name:"+name).encode())
	print("line 63")
	message = server.recv(2048)
	print("message:",message)
	tmp_key = int(message.decode("utf-8"))
	tmp_key = self_ob.diff_hullman_ex_sent(tmp_key,key)
	return tmp_key

		
def send_message(message,name,tmp_key):
	print("using key:",tmp_key)
	tmp_mess= str(self_ob.thread_encrypt(message,tmp_key))		
	tmp = json.dumps({"name" : name , "message": tmp_mess})
	#print(self_ob.thread_decrypt(tmp_mess.decode("utf-8"),key),"decoded")
	server.send(tmp.encode()) 
	print("<You>"+message)
	#time.sleep(1)  
	pass

def listen(window,de_key,k):
	sockets_list = [sys.stdin, server] 
	read_sockets = sockets_list
	while True:
		message = server.recv(2048) #problem line
		message = message.decode("utf-8")
		message_json_parse = json.loads(message)
		print("working...",message_json_parse['message'])
		message = self_ob.thread_decrypt(message_json_parse['message'],de_key)
		if (message!='\0'):
			window.update(message)
			print(("<>")+message)
		else:
			2+2

def close():
	print("closing")
	server.close() 



"""
Time log 
RHL - 3/14/19 5pm - 7:30pm (2hrs 30min)
RHL - 3/17/19 3:00- 3:47pm (47min)
RHL - 3/18/19 10am - 12:00am (1hr 42 min)
RHL - 3/18/19 12:37pm - 1:30pm (1hr)
RHL - 3/18/19 7-8pm (1hr)
RHL - 3/19/19 6-7:30pm (1hr 30 min)
RHL - 3/20/19 4-6:41pm (2hr 41min)
RHL - 3/24/19 4-6:10(2hr 10 min)
RHL - 3/26/19 9:45 -11:40pm(1hr 55min)
RHL - 3/28/19 10:45 - 12:00
RHL - 3/28/19 7:30 - 
15hr 15min total
"""
