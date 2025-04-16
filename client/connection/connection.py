import logging
import socket
import uuid

class ClientServerConnection():
    def __init__(self, host, port):
        logging.info("Initializing connection")
        self.host = host
        self.port = port
        self.client_cookie_guid = uuid.uuid4()

    def connect(self):
        logging.info("Making connection with server...")
        # get local machine name
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_to_server.connect((self.host, self.port))
        self.io_stream_client = self.socket_to_server.makefile(mode='rw')
        logging.info("Open connection with server succesfully")
    
    def close(self):
        logging.info("Closing connection with server...")
        self.socket_to_server.close()
        logging.info("Connection closed")