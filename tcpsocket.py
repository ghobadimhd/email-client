"""this module implement a tcp socket for working with smtp and pop server's"""
import socket

class TcpSocket(object):
    """
     make a tcp socket for send and reciving from pop3 server
    """
    def __init__(self):
        self.sock = None

    def connect(self, address, port):
        """Create tcp socket and connect to server

        connect to the tcp server by given address and port

        Args:
            address: ip address of server to connect
            port: port of server to connect
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))

    def send(self, data):
        """ it send data to socket

        it send data with a CRLF at the end of it to socket

        Args:
            data: the data that should be sended , it should be type of bytes
        """
        self.sock.sendall(data+b"\r\n")

    def recieve_singleline(self):
        """recieve one line of data

        recieve one line of data that ended with CRLF

        """
        data = b''
        while True:
            byte = self.sock.recv(1)
            data = data + byte
            if byte[0] == 13: # check for CR
                byte = self.sock.recv(1)
                data = data + byte
                if byte[0] == 10:# check for LF
                    break # we find CR and LF let's get out of loop
        return data

    def recieve_multiline(self, chunk=1024):
        """recive multiple line of data

        recieve multiple line of data ended by .CRLF each line ended by a CRLF
        and last line should be .CRLF

        Args:
            chunk: maximom byte of data it try to recieve each time
        """

        data = self.sock.recv(chunk)

        #if data not ended with CRLF.CRLF then get remaining
        #if there is only a .CRLF do not continue reading in that case
        #previes lines readed by recieve_singleline

        while (data[-5:] != b"\r\n.\r\n" and
               (len(data) != 3 and data != b".\r\n")):
            data = data + self.sock.recv(chunk)
        return data

    def close(self):
        """it close the socket """
        self.sock.close()
