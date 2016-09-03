import mainWindowUi
from PyQt4 import QtGui
class mainWindow (QtGui.QMainWindow): 
	def __init__(self) : 
		QtGui.QMainWindow.__init__(self)
		ui = mainWindowUi.Ui_MainWindow()
		ui.setupUi(self) 
	def intialize(self): 
		#self.readSetting()
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
		self.Config= regex.findall(setting)
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

