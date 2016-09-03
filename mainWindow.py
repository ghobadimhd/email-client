import mainWindowUi
import re
settingPath = '.setting'
from PyQt4 import QtGui
class mainWindow (QtGui.QMainWindow): 
	def __init__(self) : 
		QtGui.QMainWindow.__init__(self)
		ui = mainWindowUi.Ui_MainWindow()
		ui.setupUi(self) 
		self.initialize()
	def initialize(self): 
		self.readSetting()
		#check smtp and pop3 config for exitance and send if not 
		#resolve  ip of smtp and pop3 and add to config 
		# check for user and password 
		pass
		
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
	def inbox_refresh_button_click():
		pass 
	def inbox_remove_button_click() :
		pass
	def compose_send_button_click() : 
		pass
	def compose_clear_button_click() : 
		pass
	def inbox_listView_click(qModelIndex) : 
		pass 

