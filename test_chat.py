# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *
import encrypt_header
import datetime
import json

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow.""" 

pub_key_list = []

#Start server agruments
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
sys.argv.append('127.0.0.1')#"192.168.43.101")#IP ADDRESS
sys.argv.append(25565)#PORT
#end server argument

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number")
	exit() 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 

# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) #generates server

""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 

list_of_clients = [] 

def look_up(name):
	#pub_key look up by name
	for x in list_of_clients:
		print(x)
		if name in x:
			return str(x[1])
			pass
		pass
	pass
	print("done")
	return "0"

def look_up_addr(name):
	#addr look up by user_name
	for x in list_of_clients:
		print(x)
		if name in x:
			return x[0]
			pass
		pass
	pass
	print("didn't find")
	return "0"

def look_up_name(addr):
	#looks up user_name by addr
	for x in list_of_clients:
		if addr in x:
			return str(x[2])
			pass
		pass
	pass
	print("done")
	return "0"


def clientthread(conn, addr): 
	while True: 
			try:
				message = conn.recv(2048) 
				message = message.decode("utf-8")
				if "name:" in message:
					print(message)
					conn.send(look_up(message[5:]).encode())
				elif message:
					message_json_parse = json.loads(message)
					recive  = look_up_addr(message_json_parse['name'])
					new_message = json.dumps({"name": look_up_name(conn), "message": message_json_parse['message']})
					print(new_message)
					print(recive)
					recive.send(new_message.encode())
				else: 
					line(addr[0]+"disconect")
					"""message may have no content if the connection 
					is broken, in this case we remove the connection"""
					remove(conn)
			except:
				continue

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection):
	#don't need this function can be used for server to send everyone a message
	for clients in list_of_clients: 
		if clients==connection: #LOOK HERE !!!!!!!!!!!!!!!!!!!!!!
			try: 
				clients.send('\0'.encode()) 
			except: 
				clients.close() 
				# if the link is broken, we remove the client 
				remove(clients)
		else:
			clients.send(message)


"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection)
	print("left") 
	
def intial_handshake(conn):
	tmp_pass = ""
	while (encrypt_header.thread_encrypt(tmp_pass,S_key)!=S_password):
		print("line 161")
		conn.send("".encode())
		tmp_pass = conn.recv(2048)
		tmp_pass.decode("utf-8")
		pass
	conn.send("accept".encode())
	pass
while True: 

	"""Accepts a connection request and stores two parameters, 
	conn which is a socket object for that user, and addr 
	which contains the IP address of the client that just 
	connected"""

	conn, addr = server.accept() 

	"""Maintains a list of clients for ease of broadcasting 
	a message to all available people in the chatroom"""
	#intial handshake
	
	#end intial handshake
	# prints the address of the user that just connected 
	print (addr[0] + " connected")

	#key handshake
	dt = datetime.datetime.now()
	time =int( dt.year+dt.month+dt.day+dt.hour+dt.minute+dt.second+dt.microsecond)
	conn.send(("time_seed: "+str(time)).encode())
	# tmp_pub_key = conn.recv(2048)
	# tmp_pub_key.decode("utf-8")
	# pub_key_list.append((conn,tmp_pub_key)) 
	#end handshake
	tmp_pub_key = conn.recv(2048)
	pub_key = int(tmp_pub_key.decode("utf-8"))
	#name_input
	tmp_name = conn.recv(2048)
	tmp_name = tmp_name.decode('utf-8')
	list_of_clients.append((conn,pub_key,tmp_name))
	#conn.send(conn.encode())
	# creates and individual thread for every user 
	# that connects 
	start_new_thread(clientthread,(conn,addr))	 

conn.close() 
server.close() 

