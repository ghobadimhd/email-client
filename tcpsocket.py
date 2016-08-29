import socket 
class tcpsocket : 
	'''
	 make a tcp socket for send and reciving from pop3 server 
	'''
	def connect(self , address:str , port:int ) : # connect to server 
		self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.sock.connect((address , port)) 
	def send(self , data:bytes): # it send data to socket 
		self.sock.send(data+b"\r\n")
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
	def recvMultiLine(self , chunk:int = 1024):
		data = self.sock.recv(chunk)
		while data[-5:] != b"\r\n.\r\n" and (len(data) != 3 and data != b".\r\n" ) : # if data not ended with CRLF.CRLF then get remaining 
			data = data + self.sock.recv(chunk) 
		return data 
	def close() : 
		sock.close()


class pop3():
	"""this class implement pop3 command's """
	def __init__(self):
		self.ts = tcpsocket() 
	def connect(self ,address , port):
		self.ts.connect(address , port ) 
		return self.ts.recvSingleLine() # return hello  
	def user(self , username):
		cmd = b'user ' + username.encode() 
		self.ts.send(cmd) 
		return self.ts.recvSingleLine() 

	def pass_(self , password) :
		cmd = b'pass ' + password.encode()
		self.ts.send(cmd)
		return self.ts.recvSingleLine()
	def list(self ,msg=None):
		if msg == None : 
			cmd = b'list'
		else : 
			cmd = b'list ' + str(msg).encode()
		self.ts.send(cmd)
		if msg == None : 
			status = self.ts.recvSingleLine() # get status message 
			if len(status) >= 1  and status[0] == 43 : # if respose was positive get rest of response 
				return status +  self.ts.recvMultiLine() 
			else : 
				return status # if response was negative then just return status
		return self.ts.recvSingleLine()

	def stat(self ):
		cmd = b'stat'
		self.ts.send(cmd)
		return self.ts.recvSingleLine()
	def retr(self ,msg):
		cmd = b'retr ' + str(msg).encode()
		self.ts.send(cmd)
		return self.ts.recvMultiLine() 
	def dele(self ,msg):
		cmd = b'dele ' + str(msg).encode()
		self.ts.send()
		return self.ts.recvSingleLine()
	def noop(self ):
		self.ts.send('noop'.encode())
		return self.ts.recvSingleLine()
	def quit(self ): 
		cmd = b'quit' 
		self.ts.send(cmd)
		return self.ts.recvSingleLine()
	def top(self ,msg ,  line=1 ):
		cmd = b'top ' + str(msg).encode() +b' '  + line.encode() 
		self.ts.send(cmd)
		self.ts.recvMultiLine()
	def close(self ,):
		self.ts.close() 
	def uidl(self , msg=None):
		if msg == None : 
			cmd = b'uidl '
		else : 
			cmd = b'uidl ' + str(msg).encode()
		self.ts.send(cmd)
		if msg == None : 
			return self.ts.recvMultiLine() 
		return self.ts.recvSingleLine()
	def checkStatus(self,data:bytes , msg:list=None):
		print ('%'*40,type(data))
		status = data[0] == b'+' 
		if msg != None  :
			string = data.decode() 
			index = string.find("\r\n")
			print('index : ' , index)
			msg.clear()
			msg.append(string[1:index])
		return status 

		
