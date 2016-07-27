import socket 
class tcpsocket : 
	'''
	 make a tcp socket for send and reciving from pop3 server 
	'''
	def connect(self , address:str , port:int ) :
		self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.sock.connect((address , port))
	def send(self , data):
		self.sock.send(data)
	def strToByte(string:str ):
		return string.encode()
	def recvSingleLine(self):
		#data = self.sock.recv(1)
		data = b'' 
		while True :
			#array.append(data)
			byte = self.sock.recv(1) 
			data = data + byte 
			#data = self.sock.recv(1)
			if byte[0] == 13 : # check for CR 
				byte = self.sock.recv(1) 
				data = data + byte   
				if byte[0] == 10 :# check for LF
					break # we find CR and LF let's get out of loop 

		return data  


