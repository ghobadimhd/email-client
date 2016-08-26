import re 
class mail  :
    def __init__(self , mailParts:dict):
        self.__dict__.update(mailParts)
        

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
    def stat(statInput:str):
        regex = re.compile(".*([0-9]+) ([0-9]+)")
        match = regex.findall(statInput)
        # fix me : need exception here , checking match (len != zero)
        return (int(match[0][0]) , int(match[0][1]) )
    def uidl(uidlInput:str):
        regex = re.compile("([0-9]+) (.+)\r\n")
        matchList = regex.findall(uidlInput)
        print(matchList)
        # convert string's to number 
        output = [] 
        for record  in matchList : 
            output.append((int(record[0]) , record[1])) 
        return   output
    def retr(retrInput:str): 
        pattern = {'from':'\r\n^from: (.*)\r\n' , 
        'to':'\r\nto: *(.*)\r\n' , 
        'cc':'^\r\ncc: (.*)\r\n' , 
        'replay-to':'\r\nreplay-to: (.*)\r\n' , 
        'date':'\r\ndate: (.*)\r\n' , 
        'content-type':'\r\ncontent-type: (.*)\r\n' , 
        'message-id':'\r\nmessage-id: (.*)\r\n' , 
        'mime-version':'\r\nmime-version: (.*)\r\n' , 
        'return-path':'\r\nreturn-path: (.*)\r\n' , 
        'user-agent':'\r\nuser-agent: (.*)\r\n' , 
        'delivered-to':'\r\ndelivered-to: (.*)\r\n' , 
        'x-mailer':'\r\nx-mailer: (.*)\r\n' 
        }
        mail = {}
        for data in pattern.keys() : 
            regex = re.compile(pattern[data], re.I )
            match = regex.findall(retrInput)
            if len(match) > 0 : 
                mail[data] = match[0]
        bodyStartIndex = retrInput.find("\r\n\r\n")
        mail['body'] = retrInput[bodyStartIndex+4:]
        return mail 