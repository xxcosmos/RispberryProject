import socket


class BuildSocket(object):
    def __init__(self, host, port):
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.hostname = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.hostname)

    def get_connection(self):
        return self.connection
