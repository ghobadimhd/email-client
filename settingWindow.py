import pathlib
from configparser import ConfigParser
import setting
from PyQt4 import QtGui
from settingWindowUi import Ui_settingWindow


class SettingWindow(QtGui.QDialog):
    """Show window for editing settings"""

    def __init__(self):
        super(SettingWindow, self).__init__()
        self.ui = Ui_settingWindow()
        self.ui.setupUi(self)
        self.initialize()
        self.client_setting = ConfigParser()[setting.CONFIG_SECTION]

    def initialize(self):
        setting_file = pathlib.Path(setting.SETTINGS_PATH)

        if setting_file.exists() and setting_file.is_file():
            self.client_setting = setting.read_section()
            setting.add_missing_param(self.client_setting)

            self.ui.smtpServer_lineEdit.setText(self.client_setting['smtp_server'])
            self.ui.smtpUser_lineEdit.setText(self.client_setting['smtp_user'])
            self.ui.smtpPassword_lineEdit.setText(self.client_setting['smtp_pass'])

            self.ui.pop3Server_lineEdit.setText(self.client_setting['pop3_server'])
            self.ui.pop3User_lineEdit.setText(self.client_setting['pop3_user'])
            self.ui.pop3Password_lineEdit.setText(self.client_setting['pop3_pass'])

    def save_button_click(self):
        self.client_setting['smtp_server'] = self.ui.smtpServer_lineEdit.text()
        self.client_setting['smtp_user'] = self.ui.smtpUser_lineEdit.text()
        self.client_setting['smtp_pass'] = self.ui.smtpPassword_lineEdit.text()

        self.client_setting['pop3_server'] = self.ui.pop3Server_lineEdit.text()
        self.client_setting['pop3_user'] = self.ui.pop3User_lineEdit.text()
        self.client_setting['pop3_pass'] = self.ui.pop3Password_lineEdit.text()

        setting.write(self.client_setting)
        self.close()

    def cancel_button_click(self):
        self.close()
