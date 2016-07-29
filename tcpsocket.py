import socket 
class tcpsocket : 
	'''
	 make a tcp socket for send and reciving from pop3 server 
	'''
	def connect(self , address:str , port:int ) : # connect to server 
		self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.sock.connect((address , port)) 
	def send(self , data): # it send data to socket 
		self.sock.send(data)
	def strToByte(string:str ):
		return string.encode()
	def recvSingleLine(self):
		data = b'' 
		while True :
			byte = self.sock.recv(1) 
			data = data + byte 
			if byte[0] == 13 : # check for CR 
				byte = self.sock.recv(1) 
				data = data + byte   
				if byte[0] == 10 :# check for LF
					break # we find CR and LF let's get out of loop 

		return data 


