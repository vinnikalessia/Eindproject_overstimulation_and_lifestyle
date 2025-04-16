# Imports                             |
# ────────────────────────────────────
from streamlit_cookies_controller import CookieController
from connection.connection import ClientServerConnection
from connection.socketsManager import SocketsManager
from streamlit.components.v1 import html
from auth import authentication
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import socket
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
Auth = authentication.Auth()

user = st.experimental_user
allowed_users = Auth.load_users()

st.set_page_config(page_title="Homepage", page_icon="🏠")

# state voor buttons
if "connected" not in st.session_state:
    st.session_state.connected = False

# creates one time a SocketsManager instance for all clients
@st.cache_resource
def socket_manager() -> SocketsManager:
    return SocketsManager()

# creates a socket to connect to server
def get_connection():
    sm = socket_manager()
    controller = CookieController()
    client_cookie_guid = controller.get('client_cookie_guid')
    st.write(client_cookie_guid)
    time.sleep(5)

    if client_cookie_guid is None: # cookie is not yet in browser
        # create a new socket connection
        host = os.getenv("HOST", socket.gethostname())
        port = int(os.getenv("PORT", 8502))
        socket_connection = ClientServerConnection(host, port)
        # set client_cookie_guid in cookies
        controller.set('client_cookie_guid', socket_connection.client_cookie_guid)

        sm.add_socket(socket_connection)
    else: # cookie is already in browser
        # check if socket already exists
        socket_connection = sm.get_socket_by_cookie_guid(client_cookie_guid)
        if socket_connection is None:
            host = os.getenv("HOST", socket.gethostname())
            port = int(os.getenv("PORT", 8502))
            socket_connection = ClientServerConnection(host, port)
            controller.set('client_cookie_guid', socket_connection.client_cookie_guid)
            sm.add_socket(socket_connection)

    return socket_connection

# controle
list_sockets = socket_manager().sockets
st.write(list_sockets)

# Authentication & app                |
# ────────────────────────────────────
if not user.is_logged_in:
    st.title("Hello guest! 👋")
    st.markdown("#### ⬅️ To use this app, please log in.")
    with st.sidebar:
        st.button("Log in", on_click=st.login)
else:
    # check if user is already registered
    if user.email not in allowed_users:
        allowed_users.add(user.email)
        Auth.save_users(allowed_users)
        st.success("You’ve been registered! Changes are being saved...")
        time.sleep(3)
        st.rerun()

    # Webpage                         |
    # ────────────────────────────────
    with st.sidebar:
        st.button("Log out", on_click=st.logout)
    
    st.title(f"Welcome, {user.name or user.email}!")

    st.markdown("##### Connect and disconnect from server🔌")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        # button to connect with server
        if st.button("Connect to server", icon="🟢"):
            connect = get_connection()

    with col2:
        # button to disconnect from server
        if st.button("Close connection server", disabled=not st.session_state.connected, icon="🔴"):
            msg: dict = {"commando": "CLOSE"}
            msg: str = json.dumps(msg)
            connect = get_connection()
            connect.io_stream_client.write(f"{msg}\n")
            connect.io_stream_client.flush()
            st.session_state.connected = False
            st.components.v1.html("""
                <script>localStorage.setItem("connected", "false");</script>
            """, height=0)
            st.text("Connection closed...")
            st.cache_resource.clear()
            st.rerun()

    st.write(f"session state: {st.session_state.connected}")
    st.markdown("##### Connection status:")
    if st.session_state.connected:
        st.success("Connected to server!", icon="✅")
    else:
        st.error("Not connected to server! Please connect to the server to use this app.", icon="❌")