import re 


class mail(object):
    """this class represent a mail """

    class mailHeader(object):
        """represent header of a mail """
        def __init__(self, headerDict=None):
            if type(headerDict) is dict :
                self.__dict__.update(headerDict)

    def __init__(self,  rawMail=None):
        if type(rawMail) is bytes : 
            rawMail = rawMail.decode()
        if type(rawMail) is str : 
            headerSection = mail.findHeader(rawMail)
            self.header = mail.mailHeader(mail.parseHeaders(headerSection)) 
            self.body = mail.findBody(rawMail) 
        elif rawMail is None : 
            self.header = mail.mailHeader() 
            self.body = "" 


    def parseHeaders(headerString):
        """it parse raw header string to dictionary """
        # add exception to check headerString type (it should be string)
        headerPattern = '(.*): (.*(?:(?:\r\n\s.*)*))\r\n'
        regex = re.compile(headerPattern , re.I) 
        headers =  regex.findall(headerString)
        return dict(headers ) 

    def findBody(rawMail):
        # add exception to check mail type should be str
        index = rawMail.find('\r\n\r\n') # header and body seprated with two \r\n
        return rawMail[index+4:]

    def findHeader(rawMail):
        # add exception to check mail type should be str
        index = rawMail.find('\r\n\r\n') # header and body seprated with two \r\n
        return rawMail[:index+2]


class pop3parser : 
    '''
    this class has multiple method for parsing pop3 output 
    name of method are same as the command of pop3 
    '''
    def list(listInput:str):
        regex = re.compile("([0-9]+) ([0-9]+)")
        matchList = regex.findall(listInput)
        # convert string's to number 
        output = [] 
        for record  in matchList : 
            output.append((int(record[0]) , int(record[1]))) 
        return   output
    def stat(statInput:str):
        regex = re.compile(".*([0-9]+) ([0-9]+)")
        match = regex.findall(statInput)
        # fix me : need exception here , checking match (len != zero)
        return (int(match[0][0]) , int(match[0][1]) )
    def uidl(uidlInput:str):
        regex = re.compile("([0-9]+) (.+)\r\n")
        matchList = regex.findall(uidlInput)
        # convert string's to number 
        output = [] 
        for record  in matchList : 
            output.append((int(record[0]) , record[1])) 
        return   output
    def retr(retrInput:str): 
        
        return mail(retrInput)