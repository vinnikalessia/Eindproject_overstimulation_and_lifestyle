import threading
import logging
import json


class ClientHandler(threading.Thread):
    def __init__(self, socketclient):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient

    def run(self):
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

        logging.debug(f"CLH - Connection closed...")
        self.socket_to_client.close()
