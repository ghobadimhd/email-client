import tcpsocket
class smtp: 
	def __init__(self):
		self.ts = tcpsocket.tcpsocket()
	def conncet(self , ip:str , port:int):
		self.ts.connect(ip , port) 
		return self.ts.recvSingleLine()
	def helo(self, hostname):
		cmd =b'helo' + hostname.decode() 
		self.ts.send(cmd)
		return self.ts.recvSingleLine() 		