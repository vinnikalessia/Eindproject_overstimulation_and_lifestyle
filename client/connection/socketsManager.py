from connection.connection import ClientServerConnection
import streamlit as st
import logging
import socket
import time
import uuid
import json
import os

class SocketsManager():
    def __init__(self):
        self.sockets: list[ClientServerConnection] = []
    
    def add_socket(self, socket_connection: ClientServerConnection):
        self.sockets.append(socket_connection)
    
    def get_socket_by_cookie_guid(self, client_cookie_guid) -> ClientServerConnection:
        for socket in self.sockets:
            if socket.client_cookie_guid == client_cookie_guid:
                return socket
        return None
    
    def remove_socket(self, socket: ClientServerConnection):
        self.sockets.remove(socket)
        socket.close()

