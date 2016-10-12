import pathlib
import setting
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
		setting_file = pathlib.Path(setting.SETTINGS_PATH)

		if setting_file.exists() and setting_file.is_file():
			client_setting = setting.read_section()
			setting.add_missing_param(client_setting)

			self.ui.smtpServer_lineEdit.setText(client_setting['smtp_server'])
			self.ui.smtpUser_lineEdit.setText(client_setting['smtp_user'])
			self.ui.smtpPassword_lineEdit.setText(client_setting['smtp_pass'])

			self.ui.pop3Server_lineEdit.setText(client_setting['pop3_server'])
			self.ui.pop3User_lineEdit.setText(client_setting['pop3_user'])
			self.ui.pop3Password_lineEdit.setText(client_setting['pop3_pass'])

	def save_button_click(self):
		pass

	def cancel_button_click(self):
		pass