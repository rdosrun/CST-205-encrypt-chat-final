import math
from _thread import *
import time
class client:
	def __init__(self,s1,address):
		super(client, self).__init__()
		self.name = s1
		self.ip = address[0]
		self.port = address[1]

	def key_gen(self,tmp_seed2):#generates the private key for the usesr
		y = int(math.sin(tmp_seed2*tmp_seed2)*10000)#creates random number
		if(y<0):
			y = y*-1;
		return int(y)

	def diff_hullman_ex_sent(self,a,nb):
		#This takes the public key from the server and the private key and creates a new private key
		return (nb**a)%17737

	def diff_hullman_ex_gen(self,a):
		#generates a public key (diffy hullman gey exchange for algorthim reverence)
		n = 2305843009213693951;
		return ((n**a)%17737)

	def thread_encrypt(self,message2,key):
		#This creates parsing markers for the threading
		tmp = int(len(message2)/4)
		rmd = len(message2)%4
		place =0

		"""
		This is a fudge factor that I would 
		still need to replace a more eligant solution
		"""
		if tmp ==1:
			tmp = tmp+1
		message_parts = [None]*(tmp-1)
		
		#Creates threads for each parsed portion of 	
		for x in range(tmp-1):
			if x==tmp-2:
				start_new_thread(self.encrypt,(message2[place:],key,message_parts,place/4))
			else:
				start_new_thread(self.encrypt,(message2[place:(place+4)],key,message_parts,place/4))
				
			place=place+4#each set is of size 4 
		#This waits for all threads to finish 
		while not (message_parts[tmp-2]):
			time.sleep(1)
			pass
		blank = ""
		#combinds all threads and returns string
		for x in range(len(message_parts)):#when you enter a small message the probelm is that the tmp = 2 so for loop no go
			if isinstance(message_parts[x], str):
				blank = blank+message_parts[x]			
			pass
		return blank

	def thread_decrypt(self,message2,key):
		#parses message
		tmp = int(len(message2)/4)
		rmd = len(message2)%4
		"""
			fudge factor refer to thread_encrypt 
			for more detailed description
		"""
		if tmp == 1:
			tmp = tmp+1;
			pass
		#stores message
		message_parts = [None]*(tmp-1)
		place =0
		#takes parsed portions and starts threads to encrypt them
		for x in range(tmp-1):
			if x==tmp-2:
				start_new_thread(self.decrypt,(message2[place:],key,message_parts,place/4))
			else:
				start_new_thread(self.decrypt,(message2[place:(place+4)],key,message_parts,place/4))
			place=place+4#increments place in string

		#
		while not(message_parts[tmp-2]):
			pass
		blank = ""
		for x in range(len(message_parts)):
			if message_parts[x]==None:
				2+2
			else:
				blank = blank+message_parts[x]
			pass
		return blank
				

	def encrypt(self,message2,key,message_parts,pos):
		message = message2
		message_nums =[]
		for j in range(len(message)):
			message_nums.append(ord(message[j]))
		# 	print(ord(message[j]))
		# print("!")
		for i in range(key):
			#print(message_nums,message2)
			for j in range(len(message)):
				if(j <len(message)-1):
					#print(message_nums[j],"+",message_nums[j+1],"=",message_nums[j]+message_nums[j+1])
					message_nums[j+1] = (message_nums[j]+message_nums[j+1]);
				else:
					#print(message_nums[j],"+",message_nums[0],"=",message_nums[j]+message_nums[0])
					message_nums[0] = (message_nums[j]+message_nums[0]);
			#print(message_nums,message2)
		message = ""
		for tmp in range(len(message2)):
			message_nums[tmp] = message_nums[tmp]%55296
			message = message + chr(message_nums[tmp])
			#print(message_parts,len(message_parts))
		print(message)
		message_parts[int(pos)] = message
		#print("new",message_parts)
		#return tmp_string


	def decrypt(self,message2,key,message_parts,pos):
		message = message2
		message_nums =[]
		for j in range(len(message)):
			try:
				message_nums.append(ord(message[j]))
			except:
				continue
		tmp_length = len(message)-1
		for i in range(key,0,-1):
			#print(message_nums)
			for j in range(tmp_length,-1,-1):
				if(j<tmp_length):
					#print(message_nums[j],"-",message_nums[j+1],"=",message_nums[j]-message_nums[j+1])
					message_nums[j+1] = (message_nums[j+1]-message_nums[j]);
				else:
					message_nums[0] = (message_nums[0]-message_nums[j]);
			#print(message_nums)
		message = ""#sorry senpi
		for tmp in range(tmp_length+1):
		 	message_nums[tmp] = message_nums[tmp]%55296
		 	message = message + chr(message_nums[tmp])
		#print(message2,"adding",message_nums)
		message_parts[int(pos)] = message
		#print("new:  ",message_parts)

