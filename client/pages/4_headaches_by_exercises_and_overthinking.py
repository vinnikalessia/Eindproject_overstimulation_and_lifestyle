# Imports                             |
# ────────────────────────────────────
from connection.connection import ClientServerConnection
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
from datetime import time as dt
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Average occurences of headache in a week based on exercise hours and overthinking", page_icon="🤕")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "user" not in st.session_state:
    st.session_state.user = None

# list options exercise time
time_options = ["0:00", "0:15", "0:30", "0:45", "1:00", "1:15", "1:30", "1:45", "2:00", "2:15", "2:30", "2:45", "3:00"]

@st.cache_resource
def get_connection():
    load_dotenv()
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    socket_connection = ClientServerConnection(host, port)
    socket_connection.connect()
    return socket_connection

# convert time to float
def convert_time_to_float(time_str: str) -> float:
    if time_str == "0:00":
        return 0.0
    else:
        time_parts = time_str.split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        return hours + (minutes / 60.0)

# Authentication & app                |
# ────────────────────────────────────
# How many times could I get a headache in a week if I have x exercise hours and y overthinking?
if not st.session_state.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.error("Sorry, you can't use the app unless you are connected and logged in.", icon="❗")
    time.sleep(3)
    st.switch_page("home.py")
else:
    st.markdown(f"## What could be the average occurences of :primary-background[headaches] depending on the hours of :primary-background[exercise] and the :primary-background[overthinking score]?")
    
    col1, col2 = st.columns(2)
    with col1:
        exercise_hours = st.selectbox("How long the exercise is", time_options, index=0, key="exercise_hours")
        exercise_hours = convert_time_to_float(exercise_hours)
    with col2:
        overthinking_score = st.number_input("How much someone overthinks", min_value=1, max_value=9, value=1, help="1 being no overthinking and 9 a lot of overthinking", key="overthinking_score")
    if st.button("Confirm"):
        # send message to server with exercise hours and overthinking score as parameters
        msg: dict = {"commando": "Headache by exercise hours and overthinking", "exercise_hours": exercise_hours, "overthinking_score": overthinking_score}
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

        if data.empty:
            st.warning("No data available for the selected exercise hours and overthinking score.")
        else:
            counts = data["Headache_Frequency"].value_counts().reset_index()
            counts.columns = ["Headache_Frequency", "Count"]

            st.bar_chart(counts.set_index("Headache_Frequency"), x_label="Headache frequency", y_label="Amount of people", color="#5D848D")