# Imports                             |
# ────────────────────────────────────
from connection import connection
from auth import authentication
import streamlit as st
import logging
import socket
import time

# Setup & init                        |
# ────────────────────────────────────
Auth = authentication.Auth()

user = st.experimental_user
allowed_users = Auth.load_users()

# Authentication & app                |
# ────────────────────────────────────
# if not user.is_logged_in:
#     st.title("Hello guest! 👋")
#     st.markdown("#### ⬅️ To use this app, please log in.")
#     with st.sidebar:
#         st.button("Log in", on_click=st.login)
# else:
#     with st.sidebar:
#         st.button("Log out", on_click=st.logout)

#     if user.email not in allowed_users:
#         allowed_users.add(user.email)
#         Auth.save_users(allowed_users)
#         st.success("You’ve been registered! Changes are being saved...")
#         time.sleep(3)
#         st.rerun()
#     else:
#         st.text(f"Welcome, {user.name or user.email}!")

##########################################
import json

host = socket.gethostname()
port = 8501

if "connected" not in st.session_state:
    st.session_state.connected = False

# prevents multiple threads
@st.cache_resource
def get_cached_connection():
    connect = connection.ServerConnection()
    connect.connect()
    st.session_state.connected = True
    return connect

if st.button("Connect"):
    st.text("Connecting to server...")
    connect = get_cached_connection()
    st.text("Connected to server!")
    logging.info("Making connection with server...")

# connect = get_cached_connection()

if st.button("calculate 5 + 10", disabled=not st.session_state.connected):
    msg: dict = {"commando": "som", "getal1": 5, "getal2": 10}
    msg: str = json.dumps(msg)
    connect = get_cached_connection()
    connect.io_stream_client.write(f"{msg}\n")
    connect.io_stream_client.flush()
    res: str = connect.io_stream_client.readline().rstrip('\n')
    logging.debug(f"CLH - Sending back sum: {res}")
    st.write(f"CLH - Sending back sum: {res}")

if st.button("CLOSE", disabled=not st.session_state.connected):
    msg: dict = {"commando": "CLOSE"}
    msg: str = json.dumps(msg)
    connect = get_cached_connection()
    connect.io_stream_client.write(f"{msg}\n")
    connect.io_stream_client.flush()
    st.session_state.connected = False
    st.text("Connection closed...")
    st.cache_resource.clear()
    st.rerun()
