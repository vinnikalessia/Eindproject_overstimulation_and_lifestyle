import logging
import socket

class ServerConnection():
    def __init__(self, host=socket.gethostname(), port=8502):
        self.host = host
        self.port = port

    def connect(self):
        logging.info("Making connection with server...")
        # get local machine name
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_to_server.connect((self.host, self.port))
        self.io_stream_client = self.socket_to_server.makefile(mode='rw')
        logging.info("Open connection with server succesfully")
