# Imports                             |
# ────────────────────────────────────
from connection.connection import ClientServerConnection
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Average stress level based on sleep and overstimulated", page_icon="🫨")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "user" not in st.session_state:
    st.session_state.user = None

@st.cache_resource
def get_connection():
    load_dotenv()
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    socket_connection = ClientServerConnection(host, port)
    socket_connection.connect()
    return socket_connection

# Authentication & app                |
# ────────────────────────────────────
# What is the average stress level of people with the chosen sleep hours and overstimulated?
if not st.session_state.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.error("Sorry, you can't use the app unless you are connected and logged in.", icon="❗")
    time.sleep(3)
    st.switch_page("home.py")
else:
    st.markdown(f"## How :primary-background[stressed] are people depending on how much they :primary-background[sleep] and whether they’re :primary-background[overstimulated]?")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep_hours = st.number_input("Hours of sleep", min_value=0, max_value=24, value=0, key="sleephours")
    with col2:
        overstimulated = st.selectbox("Overstimulated?", ["Yes", "No"], key="overstimulated")

    if st.button("Confirm"):
        # send message to server with sleep hours and overstimulated as parameters
        msg: dict = {"commando": "Stress by sleep and overstimulated", "Sleep hours": sleep_hours, "Overstimulated": overstimulated}
        msg: str = json.dumps(msg)
        connect = get_connection()
        connect.io_stream_client.write(f"{msg}\n")
        connect.io_stream_client.flush()

        # get result from server
        res: str = connect.io_stream_client.readline().rstrip('\n')
        res: dict = json.loads(res)

        # convert str to json to dataframe
        str_data = res["data"]
        json_data = json.loads(str_data)
        data = pd.DataFrame(json_data)

        counts = data["Stress_Level"].value_counts().reset_index()
        counts.columns = ["Stress_Level", "Count"]

        st.bar_chart(counts.set_index("Stress_Level"), x_label="Stress level", y_label="Amount of people", color="#5D848D")