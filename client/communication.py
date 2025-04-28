from streamlit_cookies_controller import CookieController
from connection.connection import ClientServerConnection
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import socket
import time
import json
import os

@st.cache_resource(show_spinner=False)
def get_connection():
    try:
        load_dotenv()
        host = os.getenv("HOST")
        port = int(os.getenv("PORT"))
        socket_connection = ClientServerConnection(host, port)
        socket_connection.connect()
        st.session_state.connected = True
        st.session_state.state_message = "You are now connected to the server. Enjoy the app!"
        return socket_connection
    except socket.error as e:
        st.session_state.state_message = f"Connection error: {e}. Please check your connection and try again."
        time.sleep(3)
        return None
    except Exception as e:
        st.session_state.state_message = f"An error occurred: {e}. Please try again later."
        time.sleep(3)
        return None

# check if the connection is still alive
@st.fragment(run_every=3)
def check_server_connection():
    if st.session_state.connected:
        send_message("ping", {})
        response = get_response()

        if response == "pong":
            pass
        else:
            st.toast("Connection error. Please check your connection and try again.", icon="❗")
    else:
        print("Not connected to the server.")

# returns deserialized content of the response
def get_response():
    socket_connection = get_connection()
    response: str = socket_connection.io_stream_client.readline().rstrip('\n')
    response: dict = json.loads(response)
    response_data = response["response"]
    return response_data

def send_message(commando: str, data: dict) -> dict:
    socket_connection = get_connection()
    msg = json.dumps({"commando": commando.lower(), "data": data})
    socket_connection.io_stream_client.write(f"{msg}\n")
    socket_connection.io_stream_client.flush()
    print(f"Client - sent message: {msg}")
    
def send_close_message():
    send_message("close", {})
    socket_connection = get_connection()
    socket_connection.close()