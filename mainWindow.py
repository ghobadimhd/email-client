import mainWindowUi
import re
import sys
import socket
from tcpsocket import pop3
from parser import pop3parser , mail as Mail
from PyQt4 import QtGui , QtCore
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
		self.getMails()
		items = QtGui.QStandardItemModel() 
		
		for item in self.mails.keys() : 
			items.appendRow([QtGui.QStandardItem(str(item)+ ' - ' + self.mails[item].from_ + \
			 ' - ' +self.mails[item].subject)])
		self.ui.inbox_mails_listView.setModel(items)

	def inbox_remove_button_click() :
		pass
	def compose_send_button_click() : 
		pass
	def compose_clear_button_click() : 
		pass
	def inbox_listView_click(qModelIndex) : 
		pass 
	def show_error_mbox(title , message) : 
		mbox = QtGui.QMessageBox()
		mbox.setWindowTitle(title) 
		mbox.setText(message) 
		mbox.exec_()
	def getMails(self) :
		pop = pop3()
		# start connection to pop3 server 
		pop.connect(self.Config['pop3Server'] , 110) 
		response = pop.user(self.Config['pop3User'])
		if not pop.checkStatus(response) : 
			show_error_mbox('pop3 error' , response.decode()) 
			return None
		# authentication with pop3 server using basic protocol user and pass command's
		response = pop.pass_(self.Config['pop3Pass'])
		if not pop.checkStatus(response) : 
			show_error_mbox('pop3 error' , response.decode()) 
			return None
		response = pop.uidl()
		if not pop.checkStatus(response) : 
			show_error_mbox('pop3 error' , response.decode()) 
			return None
		# getting list of uidl's (message's and uidl code's)
		self.uidl = pop3parser.uidl(response.decode())
		self.mails = {}
		# get's mail content's by list of uidl's 
		for entry in self.uidl : 
			response = pop.retr(entry[0])
			if pop.checkStatus(response) :
				mail =  Mail( pop3parser.retr(response.decode()) ) 
				mail.uidl= entry[1]
				self.mails[entry[0]] = mail