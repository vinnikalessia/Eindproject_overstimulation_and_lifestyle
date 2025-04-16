# Imports                             |
# ────────────────────────────────────
from streamlit_javascript import st_javascript
from connection import connection
from auth import authentication
import streamlit as st
import pandas as pd
import socket
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Overstimulated by age", page_icon="😥")
Auth = authentication.Auth()

user = st.experimental_user
allowed_users = Auth.load_users()

# Check localStorage to restore connection state
connected_from_storage = st_javascript("localStorage.getItem('connected');")
if connected_from_storage == "true":
    st.session_state.connected = True

if "connected" not in st.session_state:
    st.session_state.connected = False
    st.components.v1.html("""
        <script>localStorage.setItem("connected", "false");</script>
    """, height=0)

@st.cache_resource
def get_cached_connection():
    host = os.getenv("HOST", socket.gethostname())
    port = int(os.getenv("PORT", 8502))
    connect = connection.ServerConnection(host, port)
    connect.connect()
    st.session_state.connected = True
    return connect

# Authentication & app                |
# ────────────────────────────────────
if not user.is_logged_in:
    # Auth.redirecting()
    pass
else:
    with st.sidebar:
        st.button("Log out", on_click=st.logout)

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

        # plot the data
        st.bar_chart(counts.set_index("Overstimulated"), color="#5D848D")