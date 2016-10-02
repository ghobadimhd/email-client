"""implement smtp command's """
import base64
import tcpsocket

class Smtp(object):
    """implemet smtp client library """

    def __init__(self):
        """it make socket """
        self.socket = tcpsocket.TcpSocket()

    def connect(self, address, port):
        """connect to smtp server by address and port

        connect to smtp server by given address and port

        Args:
            address: smtp server ip address
            port: smtp server port number

        returns:
            bytes retruned by server
        """
        self.socket.connect(address, port)
        return self.socket.recieve_singleline()

    def helo(self, hostname):
        """helo commnad as defined in rfc821

        returns:
            bytes retruned by server
        """

        cmd = b'helo ' + hostname.encode()
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def mail_from(self, sender):
        """mail from command as defined in rfc821

        for now it just get one sender

        Args:
            sender: reverse-path

        returns:
            bytes retruned by server
        """
        cmd = b'mail from:' +sender.encode()
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def rcpt_to(self, rcpt_list):
        """rcpt to command as defined in rfc821
        returns:
            bytes retruned by server
        """
        answer = {}
        for mail in rcpt_list:
            cmd = b'rcpt to:' +mail.encode()
            self.socket.send(cmd)
            answer[mail] = self.socket.recieve_singleline()
        return answer

    def data(self, mail_data):
        """send data (mail body and header) to server

        it send should called after rcpt_to command

        Args:
            mail_data: mail data including header and body

        returns:
            bytes retruned by server
        """
        response = []
        cmd = b'data'
        mail_data = mail_data.replace('\r\n.\r\n', '\r\n..\r\n')
        self.socket.send(cmd)
        first_response = self.socket.recieve_singleline()
        response.append(first_response)

        # if first response start with '3'(= 51)

        if first_response[0] == 51:
            self.socket.send(mail_data.encode())
            self.socket.send('.'.encode()) # end of mail
            response.append(self.socket.recieve_singleline())
        return response

    def quit(self):
        """quit command
        returns:
            bytes retruned by server
        """
        cmd = b'quit'
        self.socket.send(cmd)
        return self.socket.recieve_singleline()

    def auth_plain(self, username, password):
        """AUTH PLAIN CRIDIT

        authenticate ot smtp server with AUTH PLAIN method

        Args:
            username: username
            password: user password

        returns:
            bytes retruned by server
        """
        #FIXME : it should check user pass type and
        #throw exception if it's needed
        auth_string = '\x00{}\x00{}'.format(username, password).encode()
        base64_auth_string = base64.b64encode(auth_string)
        cmd = b'AUTH PLAIN ' + base64_auth_string
        self.socket.send(cmd)
        return self.socket.recieve_singleline()
