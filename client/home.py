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
st.set_page_config(page_title="Homepage", page_icon="🏠")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "user" not in st.session_state:
    st.session_state.user = None

if "state_message" not in st.session_state:
    st.session_state.state_message = None

if "error_message" not in st.session_state:
    st.session_state.error_message = None

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

def send_message(data):
    socket_connection = get_connection()
    socket_connection.io_stream_client.write(data + "\n")
    socket_connection.io_stream_client.flush()
    # Wait for a response from the server
    response = socket_connection.io_stream_client.readline().rstrip('\n')
    return response

def send_close_message():
    data = json.dumps({"commando": "CLOSE"})
    socket_connection = get_connection()
    socket_connection.io_stream_client.write(f"{data}\n")
    socket_connection.io_stream_client.flush()
    socket_connection.close()

# Authentication & app                |
# ────────────────────────────────────
if not st.session_state.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.markdown("#### To use this app, please connect to the server first and login.")
else:
    st.title(f"Welcome back! {st.session_state.user} 👋")

@st.fragment()
def connect_button():
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.session_state.connected == True:
            if st.button(":red[:material/wifi_off:] Disconnect from server"):
                with st.spinner("Disconnecting..."):
                    time.sleep(1)
                    send_close_message()
                    st.session_state.state_message = None
                    st.session_state.connected = False
                    st.session_state.user = None
                    st.cache_resource.clear()
                    st.rerun()
        else:
            if st.button(":green[:material/wifi:] Connect to server"):
                with st.spinner("Connecting..."):
                    time.sleep(1)
                    get_connection()
                    st.rerun()
    with col2:
        if st.session_state.state_message is not None:
            if "error" in st.session_state.state_message:
                st.error(st.session_state.state_message, icon="❗")
                st.cache_resource.clear()
            elif "Enjoy" in st.session_state.state_message:
                st.success(st.session_state.state_message, icon="✅")
                st.cache_resource.clear()

connect_button()

if not st.session_state.user:
    # input fields for login
    name = st.text_input(":material/person: Enter your name", key="name", disabled=not st.session_state.connected)
    password = st.text_input(":material/key: Enter your password", key="password", type="password", disabled=not st.session_state.connected)

    disabled = not st.session_state.connected or not name or not password
    help = "Please connect to the server first." if not st.session_state.connected else ""
    help = "Enter all fields" if not name or not password else help

    if st.button("Login", type="primary", disabled=disabled, help=help):
        if name and password:
            # Send the login data to the server
            data: str = json.dumps({"commando": "Login", "name": name, "password": password})
            with st.spinner("Logging in..."):
                time.sleep(1)
                response = send_message(data)
            
            if response == "Success":
                st.session_state.user = name
                st.success(f"Login successful!")
                st.rerun()
            else:
                st.error("Login failed. Please try again.")
        else:
            st.warning("Please enter both name and password.")
else:
    st.write("You are logged in.")
    