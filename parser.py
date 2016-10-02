"""This module contain's class's for
    parsing output of pop3/smtp class method's
"""

import re


class Mail(object):
    """this class represent a mail """

    class MailHeader(object):
        """represent header of a mail """
        def __init__(self, header_dict=None):
            """constractor of MailHeader class

            if header_dict passed to it , it update member of class
            with existing header's of mail

            Args:
                header_dict: a dictionary that contain
                    mail's header key/value
            """
            if isinstance(header_dict, dict):
                self.__dict__.update(header_dict)

    def __init__(self, raw_mail=None):
        if isinstance(raw_mail, bytes):
            raw_mail = raw_mail.decode()
        if isinstance(raw_mail, str):
            header_section = Mail.find_header(raw_mail)
            header_dict = Mail.parse_headers(header_section)
            self.header = Mail.MailHeader(header_dict)
            self.body = Mail.find_body(raw_mail)
        elif raw_mail is None:
            self.header = Mail.MailHeader()
            self.body = ""

    @staticmethod
    def parse_headers(header_string):
        """it parse raw header string to dictionary """
        # add exception to check header_string type (it should be string)
        header_pattern = r'(.*): (.*(?:(?:\r\n\s.*)*))\r\n'
        regex = re.compile(header_pattern, re.I)
        headers = regex.findall(header_string)
        return dict(headers)

    @staticmethod
    def find_body(raw_mail):
        """this function find body part of email

        Args:
            raw_mail: raw email string
        Retruns:
            body section of email with string type
        """

        #FIXME add exception to check mail type should be str

        #header and body seprated with two \r\n

        index = raw_mail.find('\r\n\r\n')
        return raw_mail[index+4:]

    @staticmethod
    def find_header(raw_mail):
        """this function find header part of email

        Args:
            raw_mail: raw email string
        Retruns:
            header section of email with string type
        """

        #FIXME exception to check mail type should be str

        # header and body seprated with two \r\n

        index = raw_mail.find('\r\n\r\n')
        return raw_mail[:index+2]


class Pop3Parser(object):
    '''
    this class has multiple method for parsing pop3 output
    name of method are same as the command of pop3
    '''
    @staticmethod
    def list(list_input):
        """it parse output of stat command and return list of set's """
        regex = re.compile("([0-9]+) ([0-9]+)")
        match_list = regex.findall(list_input)
        # convert string's to number
        output = []
        for record  in match_list:
            output.append((int(record[0]), int(record[1])))
        return   output

    @staticmethod
    def stat(stat_input):
        """it parse output of stat command and return list of set's """
        regex = re.compile(".*([0-9]+) ([0-9]+)")
        match = regex.findall(stat_input)
        # fix me:need exception here , checking match (len != zero)
        return (int(match[0][0]), int(match[0][1]))

    @staticmethod
    def uidl(uidl_input):
        """it parse output of uidl command and return list of set's """
        regex = re.compile("([0-9]+) (.+)\r\n")
        match_list = regex.findall(uidl_input)
        # convert string's to number
        output = []
        for record  in match_list:
            output.append((int(record[0]), record[1]))
        return   output

    @staticmethod
    def retr(retr_input):
        """it parse output of retr command and return Mail class object """
        return Mail(retr_input)
