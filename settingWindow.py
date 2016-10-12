from PyQt4 import QtGui
from settingWindowUi import Ui_settingWindow


class SettingWindow(QtGui.QMainWindow):
	"""Show window for editing settings"""

	def __init__(self):
		super(SettingWindow, self).__init__()
		self.ui = Ui_settingWindow()
		self.ui.setupUi(self)
		self.initialize()

	def initialize(self):
		pass

	def save_button_click(self):
		pass

	def cancel_button_click(self):
		pass