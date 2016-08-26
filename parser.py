import re 
class mail  :
    def __init__(self):
        self.subject = '' 
        self.body = ''
        self.to = '' 
        self.cc = '' 
        self.replayTo = '' 
        self.contentType = '' 
        self.returnPath = ''
        self.date = ''
        self.from_ = '' 
        self.messageId = ''
        self.mimeVersion = '' 
        self.contentType = '' 
        self.userAgent = ''
        self.xOriginalTo = '' 
        self.deliveredTo = '' 
        self.disposition = '' 
        self.Xmailer = ''

class pop3parser : 
    '''
    this class has multiple method for parsing pop3 output 
    name of method are same as the command of pop3 
    '''
    def list(listInput:str):
        regex = re.compile("([0-9]+) ([0-9]+)")
        matchList = regex.findall(listInput)
        print(matchList)
        # convert string's to number 
        output = [] 
        for record  in matchList : 
            output.append((int(record[0]) , int(record[1]))) 
        return   output