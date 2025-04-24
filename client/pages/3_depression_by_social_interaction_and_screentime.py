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
st.set_page_config(page_title="Average depression score based on social interaction and screen time", page_icon="😟")

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
# What could be my depression score if I have x social interactions and y screen time?
if not st.session_state.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.error("Sorry, you can't use the app unless you are connected and logged in.", icon="❗")
    time.sleep(3)
    st.switch_page("home.py")
else:
    st.markdown(f"## What could be the :primary-background[depression score] depending on amount of :primary-background[social interactions] and :primary-background[screen time]?")
    
    col1, col2 = st.columns(2)
    with col1:
        social_interaction = st.number_input("Amount of social interaction per day", min_value=0, max_value=9, value=0, help="How many :primary-badge[times] there is a social interaction in a day?", key="social_interactions")
    with col2:
        screen_time = st.number_input("Average screen time per day", min_value=0, max_value=12, value=0, help="Rounded by :primary-badge[hours]", key="screentime")
    if st.button("Confirm"):
        # send message to server with social interactions and screen time as parameters
        msg: dict = {"commando": "Depression by social interactions and screen time", "social_interaction": social_interaction, "screen_time": screen_time}
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
            st.warning("No data available for the given parameters.", icon="⚠️")
        else:
            counts = data["Depression_Score"].value_counts().reset_index()
            counts.columns = ["Depression_Score", "Count"]

            st.bar_chart(counts.set_index("Depression_Score"), x_label="Depression score", y_label="Amount of people", color="#5D848D")