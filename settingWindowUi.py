# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingWindow.ui'
#
# Created: Wed Oct 12 23:04:47 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_settingWindow(object):
    def setupUi(self, settingWindow):
        settingWindow.setObjectName(_fromUtf8("settingWindow"))
        settingWindow.resize(244, 317)
        self.gridLayout = QtGui.QGridLayout(settingWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(settingWindow)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.smtpServer_lineEdit = QtGui.QLineEdit(settingWindow)
        self.smtpServer_lineEdit.setObjectName(_fromUtf8("smtpServer_lineEdit"))
        self.horizontalLayout_3.addWidget(self.smtpServer_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(settingWindow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.smtpUser_lineEdit = QtGui.QLineEdit(settingWindow)
        self.smtpUser_lineEdit.setObjectName(_fromUtf8("smtpUser_lineEdit"))
        self.horizontalLayout_2.addWidget(self.smtpUser_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(settingWindow)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.smtpPassword_lineEdit = QtGui.QLineEdit(settingWindow)
        self.smtpPassword_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.smtpPassword_lineEdit.setReadOnly(False)
        self.smtpPassword_lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.smtpPassword_lineEdit.setObjectName(_fromUtf8("smtpPassword_lineEdit"))
        self.horizontalLayout_6.addWidget(self.smtpPassword_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.line = QtGui.QFrame(settingWindow)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(settingWindow)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.pop3Server_lineEdit = QtGui.QLineEdit(settingWindow)
        self.pop3Server_lineEdit.setObjectName(_fromUtf8("pop3Server_lineEdit"))
        self.horizontalLayout_5.addWidget(self.pop3Server_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(settingWindow)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.pop3User_lineEdit = QtGui.QLineEdit(settingWindow)
        self.pop3User_lineEdit.setObjectName(_fromUtf8("pop3User_lineEdit"))
        self.horizontalLayout_4.addWidget(self.pop3User_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(settingWindow)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.pop3Password_lineEdit = QtGui.QLineEdit(settingWindow)
        self.pop3Password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.pop3Password_lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.pop3Password_lineEdit.setObjectName(_fromUtf8("pop3Password_lineEdit"))
        self.horizontalLayout.addWidget(self.pop3Password_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.save_button = QtGui.QPushButton(settingWindow)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.horizontalLayout_7.addWidget(self.save_button)
        self.cancel_button = QtGui.QPushButton(settingWindow)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_7.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.menubar = QtGui.QMenuBar(settingWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 244, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.statusbar = QtGui.QStatusBar(settingWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))

        self.retranslateUi(settingWindow)
        QtCore.QObject.connect(self.save_button, QtCore.SIGNAL(_fromUtf8("clicked()")), settingWindow.save_button_click)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), settingWindow.cancel_button_click)
        QtCore.QMetaObject.connectSlotsByName(settingWindow)
        settingWindow.setTabOrder(self.smtpServer_lineEdit, self.smtpUser_lineEdit)
        settingWindow.setTabOrder(self.smtpUser_lineEdit, self.smtpPassword_lineEdit)
        settingWindow.setTabOrder(self.smtpPassword_lineEdit, self.pop3Server_lineEdit)
        settingWindow.setTabOrder(self.pop3Server_lineEdit, self.pop3User_lineEdit)
        settingWindow.setTabOrder(self.pop3User_lineEdit, self.pop3Password_lineEdit)
        settingWindow.setTabOrder(self.pop3Password_lineEdit, self.cancel_button)
        settingWindow.setTabOrder(self.cancel_button, self.save_button)

    def retranslateUi(self, settingWindow):
        settingWindow.setWindowTitle(_translate("settingWindow", "Setting", None))
        self.label_3.setText(_translate("settingWindow", "smtp server :", None))
        self.label_2.setText(_translate("settingWindow", "smtp user :", None))
        self.label_6.setText(_translate("settingWindow", "smtp password :", None))
        self.label_5.setText(_translate("settingWindow", "Pop3 server :", None))
        self.label_4.setText(_translate("settingWindow", "Pop3 user :", None))
        self.label.setText(_translate("settingWindow", "Pop3 password :", None))
        self.save_button.setText(_translate("settingWindow", "Save", None))
        self.cancel_button.setText(_translate("settingWindow", "Cancel", None))

