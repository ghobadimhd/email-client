import re
import sys
import socket
from parser import Pop3Parser, Mail
from PyQt4 import QtGui
from smtp import Smtp
from pop3 import Pop3
import setting
import mainWindowUi


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setting = {}
        self.mails = []
        self.uidl = []
        self.setting_path = '.setting'

        self.ui = mainWindowUi.Ui_MainWindow()
        self.ui.setupUi(self)
        self.initialize()

    def initialize(self):
        self.setting = setting.read_section()
        #check smtp and pop3 config for exitance and send if not
        if (self.setting.get('smtp_server') is None or
                self.setting.get('pop3_server') is None):
            mbox = QtGui.QMessageBox()
            mbox.setWindowTitle("cannot find server's")
            mbox.setText("There is no smtp/pop3 server .\n"
                         "Please add smtp/pop3 server to config file"
                         " (.setting) and rerun the Program.")
            mbox.exec_()
            sys.exit()
        #resolve pop3 and smtp hostname to ip
        self.setting['smtpIp'] = socket.gethostbyname(self.setting['smtp_server'])
        self.setting['pop3Ip'] = socket.gethostbyname(self.setting['pop3_server'])
        #check pop3 username and password
        if (self.setting.get('pop3_user') is None
                or self.setting.get('pop3_pass') is None):
            mbox = QtGui.QMessageBox()
            mbox.setWindowTitle("cannot find username/password for pop3 ")
            mbox.setText("There is no username/password .\n"
                         "Please add username/password to config file "
                         "(.setting) and rerun the Program.")
            mbox.exec_()
            sys.exit()

    def inbox_refresh_button_click(self):
        '''
        it is get mail's from pop3 and fill the list
        '''
        self.clear_inbox_fields()
        self.get_mails()
        items = QtGui.QStandardItemModel()
        for item in self.mails:
            items.appendRow([QtGui.QStandardItem(str(item)+ ' - ' \
                + self.mails[item].header.From \
                + ' - ' +self.mails[item].header.Subject)])
        self.ui.inbox_mails_listView.setModel(items)

    def inbox_remove_button_click(self):
        '''
        remove mail from inbox
        '''
        list_view_model = self.ui.inbox_mails_listView.selectionModel()
        selected_items = list_view_model.selectedIndexes()
        if selected_items:
            mail_number = list_view_model.selectedIndexes()[0].row() + 1
            mail_uidl = self.mails[mail_number].uidl
            if self.remove_mail_from_pop3_inbox(mail_uidl):
                #Refresh list
                self.inbox_refresh_button_click()
        else:
            self.show_error_mbox("select mail",
                                 "Please select a mail from list")

    def compose_send_button_click(self):
        '''
        it send mail through the smtp server
        '''
        mail = Mail()
        mail.header.From = self.ui.compose_from_lineEdit.text()
        mail.header.To = self.ui.compose_to_lineEdit.text()
        mail.header.Subject = self.ui.compose_subject_lineEdit.text()
        mail.body = self.ui.compose_body_textEdit.toPlainText()
        is_ok = self.send_mail(mail)
        if is_ok:
            self.compose_clear_button_click() #clear form

    def compose_clear_button_click(self):
        self.ui.compose_from_lineEdit.setText("")
        self.ui.compose_to_lineEdit.setText("")
        self.ui.compose_subject_lineEdit.setText("")
        self.ui.compose_body_textEdit.setText("")

    def inbox_listview_click(self, qmodel_index):
        '''
        show content of selected mail in TextBox's
        '''
        mail_number = qmodel_index.row() + 1
        self.clear_inbox_fields()

        self.ui.inbox_from_lineEdit.setText(self.mails[mail_number].header.From)
        self.ui.inbox_subject_lineEdit.setText(self.mails[mail_number].header.Subject)
        self.ui.inbox_body_textEdit.setText(self.mails[mail_number].body)
        self.ui.inbox_to_lineEdit.setText(self.mails[mail_number].header.To)

    def exit_menu_click(self):
        exit() 

    def setting_menu_click(self):
        pass

    def show_error_mbox(self, title, message):
        '''
        it's show message box with given title and message
        '''
        mbox = QtGui.QMessageBox()
        mbox.setWindowTitle(title)
        mbox.setText(message)
        mbox.exec_()

    def get_mails(self):
        '''
        this method get mail's from pop3 server
        and save it in self.mails and self.uidl
        self.mail structre is: [MailNumber(int), Mail(Mail)]
        '''
        pop = Pop3()
        # start connection to pop3 server
        pop.connect(self.setting['pop3_server'], 110)
        response = pop.user(self.setting['pop3_user'])
        if not pop.check_status(response):
            self.show_error_mbox('pop3 error', response.decode())
            return None
        # authentication with pop3 server
        #using basic protocol user and pass command's
        response = pop.pass_(self.setting['pop3_pass'])
        if not pop.check_status(response):
            self.show_error_mbox('pop3 error', response.decode())
            return None
        response = pop.uidl()
        if not pop.check_status(response):
            self.show_error_mbox('pop3 error', response.decode())
            return None
        # getting list of uidl's (message's and uidl code's)
        self.uidl = Pop3Parser.uidl(response.decode())
        self.mails = {}

        # get's mail content's by list of uidl's
        # enttry[0] is mail number from uidl list

        for entry in self.uidl:

            response = pop.retr(entry[0])
            if pop.check_status(response):
                mail = Pop3Parser.retr(response.decode())
                mail.uidl = entry[1] # save mail uidl in mail object
                self.mails[entry[0]] = mail
        pop.close()

    def clear_inbox_fields(self):
        self.ui.inbox_from_lineEdit.setText("")
        self.ui.inbox_subject_lineEdit.setText("")
        self.ui.inbox_body_textEdit.setText("")
        self.ui.inbox_to_lineEdit.setText("")

    def remove_mail_from_pop3_inbox(self, mail_uidl):
        '''
        it is function for removing mail from pop3 mailbox
        '''
        pop = Pop3()
        # start connection to pop3 server
        pop.connect(self.setting['pop3_server'], 110)
        response = pop.user(self.setting['pop3_user'])
        if not self.pop3_response_check(response):
            return False

        #authentication with pop3 server
        #using basic protocol user and pass command's

        response = pop.pass_(self.setting['pop3_pass'])
        if not self.pop3_response_check(response):
            return False
        response = pop.uidl()

        if not self.pop3_response_check(response):
            return False

        # getting list of uidl's (message's and uidl code's)

        uidls = Pop3Parser.uidl(response.decode())
        target_mail_number = -1
        for number, uidl in uidls:
            if uidl == mail_uidl:
                target_mail_number = number
                break
        if target_mail_number == -1:
            self.show_error_mbox('mail not found', "Cannot find selected mail in server mailbox .")
            return False
        response = pop.dele(target_mail_number)
        if not self.pop3_response_check(response):
            return False
        response = pop.quit()
        if not self.pop3_response_check(response):
            return False
        pop.close()
        return True

    def pop3_response_check(self, response):
        if not response[0] == 43:
            self.show_error_mbox('pop3 error', response.decode())
            return False
        else:
            return True

    def send_mail(self, mail):
        '''
        it connect to smtp server and send mail
        '''
        smtp = Smtp()
        response = smtp.connect(self.setting['smtpIp'], 25)
        if not self.smtp_response_check(response):
            return False
        if self.setting.get('smtpUser') and self.setting.get('smtpPass'):
            response = smtp.auth_plain(self.setting['smtpUser'], self.setting['smtpPass'])
            if not self.smtp_response_check(response):
                return False
        response = smtp.mail_from(mail.header.From)
        if not self.smtp_response_check(response):
            return False
        response = smtp.rcpt_to([mail.header.To])
        for r in response:
            if not self.smtp_response_check(response[r]):
                return False
        content = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}".format(mail.header.From,
                                                                       mail.header.To,
                                                                       mail.header.Subject,
                                                                       mail.body)
        content.replace("\r\n.\r\n", "\r\n..\r\n")
        response = smtp.data(content)
        for r in response:
            if not self.smtp_response_check(r):
                return False
        response = smtp.quit()
        if not self.smtp_response_check(response):
            return False
        return True

    def smtp_response_check(self, response):
        if  not (response[0] == 50 or response[0] == 51):
            self.show_error_mbox('smtp error', response.decode())
            return False
        else:
            return True
