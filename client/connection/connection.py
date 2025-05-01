from threading import Thread
import logging
import socket
import json
import time
import uuid

class ServerHandler(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        logging.info("Initializing connection")
        self.host = host
        self.port = port
        self.client_cookie_guid = str(uuid.uuid4())
        self.received_messages = []
        self.connected = False

    def run(self):
        # init
        self.__connect()
        while True:
            commando, data = self.wait_for_message()
            if commando == "close":
                break
            msg = {"commando": commando, "data": data}
            self.received_messages.append(msg)
        
        if self.connected is False:
            # client initiated the closing, this is the server's response
            self.io_stream.close()
            self.socket_to_server.close()
            logging.info("Connection closed")
        else:
            # server initiated the closing, I am responding
            self.connected = False
            self.send_message("close", {})
            time.sleep(1)
            self.io_stream.close()
            self.socket_to_server.close()
            logging.info("Connection closed")

    def __connect(self):
        logging.info("Making connection with server...")
        # get local machine name
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_to_server.connect((self.host, self.port))
        self.io_stream = self.socket_to_server.makefile(mode='rw')
        self.connected = True
        logging.info("Open connection with server succesfully")
    
    def close(self):
        try:
            logging.info("Closing connection with server...")
            self.connected = False
            self.send_message("close", {})
        except Exception as e:
            logging.error(f"Error closing connection: {e}")

    # returns deserialized content of the response
    def get_response(self, commando: str):
        response_data = None
        while response_data is None:
            time.sleep(1)
            if self.received_messages:
                for msg in self.received_messages:
                    if msg["commando"] == commando.lower():
                        self.received_messages.remove(msg)
                        response_data = msg["data"]
                        break
        return response_data

    def send_message(self, commando: str, data: dict) -> dict:
        msg = json.dumps({"commando": commando.lower(), "data": data})
        self.io_stream.write(f"{msg}\n")
        self.io_stream.flush()
        print(f"Client - sent message: {msg}")

    def wait_for_message(self):
        try:
            msg = ""
            while msg == "":
                msg = self.io_stream.readline().rstrip('\n')
            
            print(msg)
            msg: dict = json.loads(msg)
            commando = msg["commando"]
            data = msg["data"]
                
            return commando, data
        except Exception as e:
            logging.error(f"CLH \t- error in wait_for_message: {e}")
            return "", {}