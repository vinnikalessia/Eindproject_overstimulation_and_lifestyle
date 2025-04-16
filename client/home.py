# Imports                             |
# ────────────────────────────────────
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

# Setup & init                        |
# ────────────────────────────────────
if "connected" not in st.session_state:
    st.session_state.connected = False

@st.cache_resource
def get_connection():
    load_dotenv()
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    st.write(host, port)
    socket_connection = ClientServerConnection(host, port)
    socket_connection.connect()
    return socket_connection

def send_message(data):
    socket_connection = get_connection()
    socket_connection.io_stream_client.write(data + "\n")
    socket_connection.io_stream_client.flush()
    # Wait for a response from the server
    response = socket_connection.io_stream_client.readline()
    return response

def send_close_message():
    data = json.dumps({"commando": "CLOSE"})
    socket_connection = get_connection()
    socket_connection.io_stream_client.write(f"{data}\n")
    socket_connection.io_stream_client.flush()
    socket_connection.close()

if st.session_state.connected:
    if st.button(":red[:material/wifi_off:] Disconnect from server"):
        with st.spinner("Disconnecting..."):
            time.sleep(1)
            socket_connection = get_connection()
            send_close_message()
            st.session_state.connected = False
            st.cache_resource.clear()
            st.rerun()
else:
    if st.button(":green[:material/wifi:] Connect to server"):
        with st.spinner("Connecting..."):
            time.sleep(1)
            socket_connection = get_connection()
            st.session_state.connected = True
            st.rerun()

name = st.text_input(":material/person: Enter your name", key="name", disabled=not st.session_state.connected)
pswd = st.text_input(":material/key: Enter your password", key="pswd", disabled=not st.session_state.connected)

disabled = not st.session_state.connected or not name or not pswd
help = "Please connect to the server first." if not st.session_state.connected else ""
help = "Enter all fields" if not name or not pswd else help

if st.button("Login", type="primary", disabled=disabled, help=help):
    if name and pswd:
        # Send the login data to the server
        data = json.dumps({"commando": "Login", "name": name, "password": pswd})
        with st.spinner("Logging in..."):
            time.sleep(1)
            response = send_message(data)
        st.write(response)
    else:
        st.warning("Please enter both name and password.")