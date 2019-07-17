import socket


class BuildSocket(object):
    def __init__(self, host, port, is_video=False):
        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        if is_video:
            self.connection = self.connection.makefile('rb')

    def get_connection(self):
        return self.connection
    #
    # def send_msg(self, msg):
    #     self.server_socket.sendall(msg.encode('utf-8'))
