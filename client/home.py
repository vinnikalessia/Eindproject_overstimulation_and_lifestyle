# Imports                             |
# ────────────────────────────────────
from connection import connection
from auth import authentication
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
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
import os

host = os.getenv("HOST")
port = os.getenv("PORT")

if "connected" not in st.session_state:
    st.session_state.connected = False

# prevents multiple threads
@st.cache_resource
def get_cached_connection():
    connect = connection.ServerConnection()
    connect.connect()
    st.session_state.connected = True
    return connect

# connect with server
if st.button("Connect"):
    connect = get_cached_connection()

# How many people are overstimulated with the chosen age?
if st.number_input("Overstimulated by age", min_value=0, max_value=100, value=0, disabled=not st.session_state.connected, key="number_input"):
    # send message to server with age as parameter
    age = st.session_state.number_input
    msg: dict = {"commando": "Overstimulated by age", "Age": age}
    msg: str = json.dumps(msg)
    connect = get_cached_connection()
    connect.io_stream_client.write(f"{msg}\n")
    connect.io_stream_client.flush()

    # get result from server
    res: str = connect.io_stream_client.readline().rstrip('\n')
    res: dict = json.loads(res)
    st.write(f"Of {res['total']} people, {res['overstimulated']} are overstimulated at the age {age}")

    # convert str to json to dataframe
    str_data = res["data"]
    json_data = json.loads(str_data)
    data = pd.DataFrame(json_data)

    # Replace 0/1 with No/Yes
    data["Overstimulated"] = data["Overstimulated"].replace({0: "No", 1: "Yes"})

    # Count how many people are overstimulated or not
    counts = data["Overstimulated"].value_counts().reset_index()
    counts.columns = ["Overstimulated", "Count"]

    st.bar_chart(counts.set_index("Overstimulated"), color="#5D848D")


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
