import tcpsocket
class smtp: 
	def __init__(self):
		self.ts = tcpsocket.tcpsocket()
	def conncet(self , ip:str , port:int):
		self.ts.connect(ip , port) 
		return self.ts.recvSingleLine()
	def helo(self, hostname):
		cmd =b'helo ' + hostname.encode() 
		self.ts.send(cmd)
		return self.ts.recvSingleLine() 	
	def mailFrom(self , sender:str):
		cmd = b'mail from:' +sender.encode()
		self.ts.send(cmd)
		return self.ts.recvSingleLine()
	def rcptTo(self, rcptList):
		answer = {} 
		for mail in rcptList : 
			cmd = b'rcpt to:' +mail.encode()
			self.ts.send(cmd)
			answer[mail] = self.ts.recvSingleLine()
		return answer
	def data(self, mailBody:str):
		cmd = b'data' 
		mailBody = mailBody.replace('\r\n.\r\n','\r\n..\r\n')
		self.ts.send(cmd)
		self.ts.send(mailBody.encode())
		self.ts.send('.'.encode())# end of mail 
		return self.ts.recvSingleLine()