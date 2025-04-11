from dotenv import load_dotenv
from threading import Thread
import threading
import logging
import socket
import json
import os

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.list_clients = []
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = int(os.getenv("PORT"))
        # bind to the port
        self.serversocket.bind((host, port))
        # queue up to 5 requests
        self.serversocket.listen(5)
    
    def run(self):
        while True:
            try:
                logging.info("Server: waiting for a client...")
                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                logging.info(f"Server: Got a connection from {addr})")
                clh = ClientHandler(socket_to_client)
                self.list_clients.append(clh)
                clh.start()
                logging.info(f"Server: ok, clienthandler started. Current Thread count: {threading.active_count()}.")
                logging.info(f"aantal clienthandlers: {len(self.list_clients)}")
            except Exception as e:
                logging.error(f"Server: error in server thread: {e}")
                break

class ClientHandler(Thread):
    def __init__(self, socket_to_client):
        Thread.__init__(self)
        self.socket_to_client = socket_to_client
        threads: list[Thread] = threading.enumerate()

        self.server_thread = None
        for thread in threads:
            if isinstance(thread, Server):
                self.server_thread = thread
                break

    def run(self):
        try:
            io_stream_client = self.socket_to_client.makefile(mode='rw')
            logging.info("CLH - started & waiting...")
            # waiting for first commando
            msg: str = io_stream_client.readline().rstrip('\n')
            msg: dict = json.loads(msg)
            commando = msg["commando"]

            while commando != "CLOSE":
                logging.debug(f"CLH - Number 1: {msg['getal1']}")
                logging.debug(f"CLH - Number 2: {msg['getal2']}")

                sum = int(msg["getal1"]) + int(msg["getal2"])
                io_stream_client.write(f"{sum}\n")
                io_stream_client.flush()
                logging.debug(f"CLH - Sending back sum: {sum}")

                # waiting for new commando
                msg: str = io_stream_client.readline().rstrip('\n')
                msg: dict = json.loads(msg)
                commando = msg["commando"]
            self.server_thread.list_clients.remove(self)
        except Exception as e:
            logging.error(f"CLH - error in clienthandler thread: {e}")


server = Server()
server.start()