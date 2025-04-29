from dotenv import load_dotenv
from threading import Thread
from search import Search
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
        self.clienthandlers: list[ClientHandler] = [] # all clienthandler threads also the ones streamlit creates
        self.clients: list = []
        
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
                logging.info("Server - waiting for a client...")
                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                logging.info(f"Server - got a connection from {addr})")
                clh = ClientHandler(socket_to_client, addr)
                self.clienthandlers.append(clh)
                clh.start()
                logging.info(f"Server - ok, clienthandler started. Current Thread count: {threading.active_count()}.")
                logging.info(f"Server - counts clienthandlers: {len(self.clienthandlers)}")
            except Exception as e:
                logging.error(f"Server - error in server thread: {e}")
                break

    def get_clients(self):
        return self.clients

class ClientHandler(Thread):
    def __init__(self, socket_to_client, addr):
        Thread.__init__(self)
        self.socket_to_client = socket_to_client
        threads: list[Thread] = threading.enumerate()
        self.io_stream_client = self.socket_to_client.makefile(mode='rw')
        self.addr = addr

        self.server_thread = None
        for thread in threads:
            if isinstance(thread, Server):
                self.server_thread: Server = thread
                break

    # response can be str, data, ...
    def send_response(self, response_data):
        '''
        Response data should be something that is serializable to JSON.
        This includes dict, list, str, int, float, bool, and None.
        '''
        response: str = json.dumps({"response": response_data})
        logging.info(f"CLH \t- sent response: {response}")
        self.io_stream_client.write(f"{response}\n")
        self.io_stream_client.flush()

    def wait_for_message(self):
        try:
            msg = ""
            while msg == "":
                msg = self.io_stream_client.readline().rstrip('\n')
            
            print(msg)
            msg: dict = json.loads(msg)
            commando = msg["commando"]
            data = msg["data"]
                
            return commando, data
        except Exception as e:
            logging.error(f"CLH \t- error in wait_for_message: {e}")
            return "", {}

    def run(self):
        try:
            logging.info("CLH \t- started & waiting...")
            commando, data = self.wait_for_message()

            while commando != "close":
                if commando == "overstimulated by age":
                    # Step 1: parameters from client
                    age = data["age"]

                    # Step 2: execute search query
                    total, overstimulated, df = search.overstimulated_by_age(age)
                    
                    # Step 3: convert to serializable format
                    res: dict = {"total": total, "overstimulated": overstimulated, "dataframe": df.to_dict(orient="records")}

                    # Step 4: send response to client
                    self.send_response(res)

                elif commando == "stress by sleep and overstimulated":
                    # Step 1: parameters from client
                    sleep_hours = data["sleep_hours"]
                    overstimulated = data["overstimulated"]

                    # Step 2: execute search query
                    mode_values, df = search.stress_by_sleep_and_overstimulated(sleep_hours, overstimulated)

                    # Step 3: convert to serializable format
                    res: dict = {"mode_values": mode_values, "dataframe": df.to_dict(orient="records")}

                    # Step 4: send response to client
                    self.send_response(res)

                elif commando == "depression by social interactions and screen time":
                    # Step 1: parameters from client
                    social_interaction = data["social_interaction"]
                    screen_time = data["screen_time"]

                    # Step 2: execute search query
                    mode_values, df = search.depression_by_social_interactions_and_screen_time(social_interaction, screen_time)

                    # Step 3: convert to serializable format
                    res: dict = {"mode_values": mode_values, "dataframe": df.to_dict(orient="records")}

                    # Step 4: send response to client
                    self.send_response(res)
                    
                elif commando == "headache by exercise hours and overthinking":
                    # Step 1: parameters from client
                    exercise_hours = data["exercise_hours"]
                    overthinking_score = data["overthinking_score"]

                    # Step 2: execute search query
                    mode_values, df = search.headache_by_exercise_hours_and_overthinking(exercise_hours, overthinking_score)
                    
                    # Step 3: convert to serializable format
                    res: dict = {"mode_values": mode_values, "dataframe": df.to_dict(orient="records")}

                    # Step 4: send response to client
                    self.send_response(res)
                
                elif commando == "login":
                    # Step 1: parameters from client
                    # prevents error if no name or password is given
                    password = data.get("password")
                    name = data.get("name")

                    with open("../server/users.json", "r", encoding="utf-8") as f:
                        users: list[dict] = json.load(f)

                    # Step 2: check if name and password are in users.json
                    found = False
                    for user in users:
                        if user["name"] == name and user["password"] == password:
                            found = True
                            # add user to clients
                            # self.server_thread.clients.append(name)
                            # add clh to clients
                            self.server_thread.clients.append(self)
                            break

                    # Step 3: send response to client
                    self.send_response("Success" if found else "Failed")
                
                elif commando == "ping":
                    self.send_response("pong")
                
                commando, data = self.wait_for_message()

            # Remove logged-in user when disconnecting
            logging.info(f"CLH \t- client: clienthandlers before{self.server_thread.clienthandlers}")
            logging.info(f"CLH \t- client: clients before {self.server_thread.clients}")

            # close the connection
            self.server_thread.clienthandlers.remove(self)
            if self in self.server_thread.clients:
                # remove the client from the clients list
                self.server_thread.clients.remove(self)
            # and remove all clients that aren't in the clients list
            for thread in self.server_thread.clienthandlers:
                if thread not in self.server_thread.clients:
                    self.server_thread.clienthandlers.remove(thread)
            self.socket_to_client.close()

            # current thread is:
            logging.info(f"CLH \t- client: current thread: {threading.current_thread()}")

            logging.info(f"CLH \t- client: clienthandlers after{self.server_thread.clienthandlers}")
            logging.info(f"CLH \t- client: clients after{self.server_thread.clients}")
        except Exception as e:
            logging.error(f"CLH \t- error in clienthandler thread: {e}")
            raise e

    def __repr__(self):
        return f"ClientHandler({self.addr})"

# is going to run only when you run server.py directly
# not when you import it in another file
# if __name__ == "__main__":
#     server = Server()
#     server.start()