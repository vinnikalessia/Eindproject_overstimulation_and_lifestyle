#Onderstaande lijnen zijn enkel nodig wanneer je test in Visual Studio Code
import sys 
from pathlib import Path 
print(sys.path[0]) 
sys.path[0] = str(Path(sys.path[0]).parent) #uitvoeringspad wordt op niveau van parent-map gezet 
#print(sys.path[0]) #test


import logging
import socket
# create a socket object
import threading

from server.clienthandler import ClientHandler


logging.basicConfig(level=logging.DEBUG)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8502

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

list_clients = []

# van deze file ene klasse maken en port, host en lijst properties maken

while True:
    logging.info("Server: waiting for a client...")

    # establish a connection
    socket_to_client, addr = serversocket.accept()

    logging.info(f"Server: Got a connection from {addr})")
    clh = ClientHandler(socket_to_client)
    list_clients.append(clh)
    clh.start()
    logging.info(f"Server: ok, clienthandler started. Current Thread count: {threading.active_count()}.")
    logging.info(f"aantal clienthandlers: {len(list_clients)}")
