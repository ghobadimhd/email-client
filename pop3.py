from tcpsocket import TcpSocket


class Pop3(object):
    """this class implement pop3 command's """
    def __init__(self):
        self.socket = TcpSocket()

    def connect(self, address, port):
        self.socket.connect(address, port)
        return self.socket.recieve_singleline()

    def user(self, username):
        cmd = b'user ' + username.encode()
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def pass_(self, password):
        cmd = b'pass ' + password.encode()
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def list(self, msg=None):
        if msg == None:
            cmd = b'list'
        else:
            cmd = b'list ' + str(msg).encode()
        self.socket.send(cmd)
        if msg == None:
            status = self.socket.recieve_singleline()

            # get status message
            # if respose was positive get rest of response

            if len(status) >= 1  and status[0] == 43:
                return status +  self.socket.recieve_multiline()
            else:
                return status # if response was negative then just return status
        return self.socket.recieve_singleline()

    def stat(self):
        cmd = b'stat'
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def retr(self, msg):
        cmd = b'retr ' + str(msg).encode()
        self.socket.send(cmd)

        # get status message
        # if respose was positive get rest of response

        status = self.socket.recieve_singleline()
        if len(status) >= 1  and status[0] == 43:
            return status +  self.socket.recieve_multiline()
        else:
            return status

    def dele(self, msg):
        cmd = b'dele ' + str(msg).encode()
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def noop(self):
        self.socket.send('noop'.encode())
        return self.socket.recieve_singleline()

    def quit(self):
        cmd = b'quit'
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def top(self, msg, line=1):
        cmd = b'top ' + str(msg).encode() +b' '  + str(line).encode()
        self.socket.send(cmd)

        # get status message
        # if respose was positive get rest of response

        status = self.socket.recieve_singleline()
        if len(status) >= 1  and status[0] == 43:
            return status +  self.socket.recieve_multiline()
        else:
            return status
        self.socket.recieve_multiline()

    def close(self):
        self.socket.close()

    def uidl(self, msg=None):
        if msg == None:
            cmd = b'uidl '
        else:
            cmd = b'uidl ' + str(msg).encode()
        self.socket.send(cmd)
        if msg == None:

            # get status message
            # if respose was positive get rest of response

            status = self.socket.recieve_singleline()
            if len(status) >= 1  and status[0] == 43:
                return status +  self.socket.recieve_multiline()
            else:
                return status
        return self.socket.recieve_singleline()
    @staticmethod
    def check_status(data, msg=None):
        status = data[0] == 43
        if msg != None:
            string = data.decode()
            index = string.find("\r\n")
            msg.clear()
            msg.append(string[1:index])
        return status
