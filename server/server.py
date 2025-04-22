from dotenv import load_dotenv
from threading import Thread
from search import Search
import pandas as pd
import threading
import logging
import socket
import json
import os

load_dotenv()
search = Search()

logging.basicConfig(level=logging.DEBUG)

class Server(Thread):
    def __init__(self):
        # initialize the thread, list of clients and read data
        Thread.__init__(self)
        self.list_clients = []
        self.data = pd.read_csv("./dataset/dataset.csv")
        
        # creating socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()
        # port = int(os.getenv("PORT"))
        host = "127.0.0.1"
        port = int(os.getenv("PORT"))

        # bind to the port and queue up to 5 requests
        self.serversocket.bind((host, port))
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
                if commando == "Overstimulated by age":
                    logging.debug(f"CLH  SEARCH: count overstimulated people of certain age.")
                    # get message/parameter from client
                    Age = msg["Age"]
                    logging.debug(f"CLH  \tchosen age: {Age}")

                    total, overstimulated, data = search.overstimulated_by_age(self.server_thread.data, Age)
                    logging.debug(f"CLH  \t{overstimulated} of {total} people are overstimulated at the age of {Age}.")
                    
                    res: dict = {"total": total, "overstimulated": overstimulated, "data": data}
                    res: str = json.dumps(res)
                    io_stream_client.write(f"{res}\n")
                    io_stream_client.flush()
                elif commando == "Stress by sleep and overstimulated":
                    logging.debug(f"CLH  SEARCH: average stress level of people with certain sleep hours and overstimulated.")
                    # get message/parameter from client
                    sleep_hours = msg["Sleep hours"]
                    overstimulated = msg["Overstimulated"]
                    logging.debug(f"CLH  \tchosen sleep hours: {sleep_hours}, overstimulated: {overstimulated}")

                    data = search.stress_by_sleep_and_overstimulated(self.server_thread.data, sleep_hours, overstimulated)

                    res: dict = {"data": data}
                    res: str = json.dumps(res)
                    io_stream_client.write(f"{res}\n")
                    io_stream_client.flush()
                elif commando == "Depression by social interactions and screen time":
                    logging.debug(f"CLH  SEARCH: depression score of people with certain social interactions and screen time.")
                    # get message/parameter from client
                    social_interaction = msg["social_interaction"]
                    screen_time = msg["screen_time"]
                    logging.debug(f"CLH  \tsocial interactions: {social_interaction}, screen time: {screen_time}")

                    data = search.depression_by_social_interactions_and_screen_time(self.server_thread.data, social_interaction, screen_time)
                    res: dict = {"data": data}
                    res: str = json.dumps(res)
                    io_stream_client.write(f"{res}\n")
                    io_stream_client.flush()
                elif commando == "Headache by exercise hours and overthinking":
                    logging.debug(f"CLH  SEARCH: headache score of people with certain exercise hours and overthinking.")
                    # get message/parameter from client
                    exercise_hours = msg["exercise_hours"]
                    overthinking_score = msg["overthinking_score"]
                    logging.debug(f"CLH  \texercise hours: {exercise_hours}, overthinking score: {overthinking_score}")

                    data = search.headache_by_exercise_hours_and_overthinking(self.server_thread.data, exercise_hours, overthinking_score)
                    res: dict = {"data": data}
                    res: str = json.dumps(res)
                    io_stream_client.write(f"{res}\n")
                    io_stream_client.flush()
                    ...
                elif commando == "Login":
                    name = msg["name"]
                    password = msg["password"]
                    logging.debug(f"CLH  \tLogin: {name}")

                    with open("./server/allowed_users.json", "r", encoding="utf-8") as f:
                        allowed_users = json.load(f)

                    for user in allowed_users["users"]:
                        if user["name"] == name and user["password"] == password:
                            logging.debug(f"CLH  \tLogin successful for {name}")
                            io_stream_client.write(f"Success\n")
                            io_stream_client.flush()
                            break
                        else:
                            logging.debug(f"CLH  \tLogin failed for {name}")
                            io_stream_client.write(f"Failed\n")
                            io_stream_client.flush()
                # waiting for new commando
                msg: str = io_stream_client.readline().rstrip('\n')
                msg: dict = json.loads(msg)
                commando = msg["commando"]
            
            # close the connection
            logging.info(f"CLH - closing connection with {self.socket_to_client.getpeername()}")
            self.server_thread.list_clients.remove(self)
        except Exception as e:
            logging.error(f"CLH - error in clienthandler thread: {e}")


server = Server()
server.start()