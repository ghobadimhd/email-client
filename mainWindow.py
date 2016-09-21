import mainWindowUi
import re
import sys
import socket
from tcpsocket import pop3
from parser import pop3parser , mail as Mail
from PyQt4 import QtGui , QtCore
from smtp import smtp
settingPath = '.setting'

class mainWindow (QtGui.QMainWindow): 
	def __init__(self) : 
		QtGui.QMainWindow.__init__(self)
		self.ui = mainWindowUi.Ui_MainWindow()
		self.ui.setupUi(self) 
		self.initialize()
	def initialize(self): 
		self.Config = {}
		self.readSetting()
		#check smtp and pop3 config for exitance and send if not
		if self.Config.get('smtpServer') is None or self.Config.get('pop3Server') is None :
			mbox = QtGui.QMessageBox()
			mbox.setWindowTitle("cannot find server's")
			mbox.setText("There is no smtp/pop3 server .\nPlease add smtp/pop3 server to config file (.setting) and rerun the Program.")
			mbox.exec_()
			sys.exit()
 		#resolve pop3 and smtp hostname to ip 
		self.Config['smtpIp'] = socket.gethostbyname(self.Config['smtpServer'])
		self.Config['pop3Ip'] = socket.gethostbyname(self.Config['pop3Server'])
		#check pop3 username and password 
		if self.Config.get('pop3User') is None or self.Config.get('pop3Pass') is None :
			mbox = QtGui.QMessageBox()
			mbox.setWindowTitle("cannot find username/password for pop3 ")
			mbox.setText("There is no username/password .\nPlease add username/password to config file (.setting) and rerun the Program.")
			mbox.exec_()
			sys.exit() 


	def readSetting(self) : 
		global settingPath
		with open(settingPath , 'r') as file : 
			temp = file.readlines()
			setting = ''
			for line in temp :
				setting = setting + line 
			del temp  
		regex = re.compile('(.*):(.*)')
		keyValue = regex.findall(setting)
		config = {}
		for  param in keyValue : 
			config[param[0]] = param[1]
		self.Config= config


	def inbox_refresh_button_click(self):
		'''
		it is get mail's from pop3 and fill the list 
		'''
		self.Clear_inbox_fields()
		self.getMails()
		items = QtGui.QStandardItemModel() 
		
		for item in self.mails.keys() : 
			items.appendRow([QtGui.QStandardItem(str(item)+ ' - ' \
				+ self.mails[item].from_ \
				+ ' - ' +self.mails[item].subject)])
		self.ui.inbox_mails_listView.setModel(items)

	def inbox_remove_button_click(self) :
		'''
		remove mail from inbox 
		'''
		selectedItems = self.ui.inbox_mails_listView.selectionModel().selectedIndexes()
		if selectedItems :
			mailNumber = self.ui.inbox_mails_listView.selectionModel().selectedIndexes()[0].row() + 1 
			mailUidl = self.mails[mailNumber].uidl
			if self.remove_mail_from_pop3_inbox(mailUidl):
				#Refresh list 
				self.inbox_refresh_button_click()
		else : 
			self.show_error_mbox('select mail', 'Please select a mail from list')
	def compose_send_button_click(self) : 
		'''
		it send mail through the smtp server 
		'''
		mail = Mail()
		mail.from_ = self.ui.compose_from_lineEdit.text()
		mail.to = self.ui.compose_to_lineEdit.text()
		mail.subject = self.ui.compose_subject_lineEdit.text() 
		mail.body = self.ui.compose_body_textEdit.toPlainText()
		ok = self.send_mail(mail)
		if ok : 
			#clear form 
			self.compose_clear_button_click()
	def compose_clear_button_click(self) : 
		self.ui.compose_from_lineEdit.setText("")
		self.ui.compose_to_lineEdit.setText("")
		self.ui.compose_subject_lineEdit.setText("") 
		self.ui.compose_body_textEdit.setText("")
	def inbox_listView_click(self ,qModelIndex) : 
		'''
		show content of selected mail in TextBox's 
		'''
		mailNumber = qModelIndex.row() + 1 
		self.Clear_inbox_fields()

		self.ui.inbox_from_lineEdit.setText(self.mails[mailNumber].from_)
		self.ui.inbox_subject_lineEdit.setText(self.mails[mailNumber].subject)
		self.ui.inbox_body_textEdit.setText(self.mails[mailNumber].body)
		self.ui.inbox_to_lineEdit.setText(self.mails[mailNumber].to)

	def show_error_mbox(self ,title , message) : 
		'''
		it's show message box with given title and message 
		'''
		mbox = QtGui.QMessageBox()
		mbox.setWindowTitle(title) 
		mbox.setText(message) 
		mbox.exec_()
	def getMails(self) :
		'''
		this method get mail's from pop3 server and save it in self.mails and self.uidl
		self.mail structre is : [MailNumber(int) , Mail(Mail)]
		'''
		pop = pop3()
		# start connection to pop3 server 
		pop.connect(self.Config['pop3Server'] , 110) 
		response = pop.user(self.Config['pop3User'])
		if not pop.checkStatus(response) : 
			self.show_error_mbox('pop3 error' , response.decode()) 
			return None
		# authentication with pop3 server using basic protocol user and pass command's
		response = pop.pass_(self.Config['pop3Pass'])
		if not pop.checkStatus(response) : 
			self.show_error_mbox('pop3 error' , response.decode()) 
			return None
		response = pop.uidl()
		if not pop.checkStatus(response) : 
			self.show_error_mbox('pop3 error' , response.decode()) 
			return None
		# getting list of uidl's (message's and uidl code's)
		self.uidl = pop3parser.uidl(response.decode())
		self.mails = {}
		# get's mail content's by list of uidl's 
		for entry in self.uidl : 
			response = pop.retr(entry[0]) # retrive mail (enttry[0] is mail number from uidl list)
			if pop.checkStatus(response) :
				mail =  Mail( pop3parser.retr(response.decode()) ) 
				mail.uidl= entry[1] # save mail uidl in mail object 
				self.mails[entry[0]] = mail
		pop.close()
	def Clear_inbox_fields(self):
		self.ui.inbox_from_lineEdit.setText("")
		self.ui.inbox_subject_lineEdit.setText("")
		self.ui.inbox_body_textEdit.setText("")
		self.ui.inbox_to_lineEdit.setText("")
	def remove_mail_from_pop3_inbox(self, mailUidl):
		'''
		it is function for removing mail from pop3 mailbox 
		'''
		pop = pop3()
		# start connection to pop3 server 
		pop.connect(self.Config['pop3Server'] , 110) 
		response = pop.user(self.Config['pop3User'])
		if not self.pop3_Response_check(response) :
			return False
		# authentication with pop3 server using basic protocol user and pass command's
		response = pop.pass_(self.Config['pop3Pass'])
		if not self.pop3_Response_check(response) :
			return False
		response = pop.uidl()
		if not self.pop3_Response_check(response) :
			return False
		# getting list of uidl's (message's and uidl code's)
		uidls = pop3parser.uidl(response.decode())
		targetMailNumber = -1 
		for number , uidl in uidls : 
			if uidl == mailUidl : 
				targetMailNumber = number
				break
		if targetMailNumber == -1 : 
			self.show_error_mbox('mail not found', "Cannot find selected mail in server mailbox .")
			return False
		response = pop.dele(targetMailNumber)
		if not self.pop3_Response_check(response) :
			return False
		esponse = pop.quit()
		if not self.pop3_Response_check(response) :
			return False
		pop.close()
		return True
	def pop3_Response_check(self , response):
		if not response[0] == 43 : 
			self.show_error_mbox('pop3 error' , response.decode()) 
			return False
		else :
			return True 
	def send_mail(self, mail ):
		'''
		it connect to smtp server and send mail 
		'''
		Smtp = smtp()
		response = Smtp.connect(self.Config['smtpIp'] , 25) 
		if not self.smtp_response_check(response) : 
			return False
		response = Smtp.mailFrom(mail.from_) 
		if not self.smtp_response_check(response) : 
			return False
		response = Smtp.rcptTo([mail.to]) 
		for r in response.keys() :
			if not self.smtp_response_check(response[r]) : 
				return False
		content = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}"\
			.format(mail.from_ , mail.to , mail.subject , mail.body) # this should implemented in Mail class
		content.replace("\r\n.\r\n", "\r\n..\r\n")
		response = Smtp.data(content) 
		for r in response:
			if not self.smtp_response_check(r) : 
				return False
		response = Smtp.quit() 
		if not self.smtp_response_check(response) : 
			return False
		return True


	def smtp_response_check(self , response):
		if  not (response[0] == 50 or  response[0] == 51 ): 
			self.show_error_mbox('smtp error' , response.decode()) 
			return False
		else :
			return True 

