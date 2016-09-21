import tcpsocket
import base64
class smtp: 
	def __init__(self):
		self.ts = tcpsocket.tcpsocket()
	def connect(self , ip:str , port:int):
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
		response = [] 
		cmd = b'data' 
		mailBody = mailBody.replace('\r\n.\r\n','\r\n..\r\n')
		self.ts.send(cmd)
		firstResponse = self.ts.recvSingleLine()
		response.append(firstResponse)
		if firstResponse[0] == 51 : # if first response start with '3'(= 51)
			self.ts.send(mailBody.encode())
			self.ts.send('.'.encode())# end of mail 
			response.append(self.ts.recvSingleLine())
		return response
	def quit(self):
		cmd =b'quit'
		self.ts.send(cmd)
		return self.ts.recvSingleLine()
	def authPlain(self,username,password):
		#fix me : it should check user pass type and throw exception if it's needed 
		AuthString = '\x00{}\x00{}'.format(username, password).encode()
		base64AuthString = base64.b64encode(AuthString)
		cmd = b'AUTH PLAIN ' + base64AuthString
		self.ts.send(cmd)
		return self.ts.recvSingleLine() 