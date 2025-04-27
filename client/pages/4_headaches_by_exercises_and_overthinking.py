# Imports                             |
# ────────────────────────────────────
from communication import get_connection, send_message, send_close_message, check_server_connection, get_response
from connection.connection import ClientServerConnection
from datetime import time as dt
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Average occurences of headache in a week based on exercise hours and overthinking", page_icon="🤕", layout="wide")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "user" not in st.session_state:
    st.session_state.user = None

check_server_connection()

# list options exercise time
time_options = ["0:00", "0:15", "0:30", "0:45", "1:00", "1:15", "1:30", "1:45", "2:00", "2:15", "2:30", "2:45", "3:00"]

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
    
    # some white space
    st.container(border=False, height=16)

    col1, col2, col3 = st.columns([2.5, 1, 5])

    with col1:
        coli1, coli2 = st.columns(2)
        with coli1:
            exercise_hours = st.selectbox("Duration exercise", time_options, index=0, help="Duration of exercise :primary-badge[per day]", key="exercise_hours")
            exercise_hours = convert_time_to_float(exercise_hours)
        with coli2:
            overthinking_score = st.number_input("Level overthinking", min_value=1, max_value=9, value=1, help="1 is :primary-badge[no overthinking] and 9 is :primary-badge[a lot of overthinking]", key="overthinking_score")
        
        if st.button("Confirm", key="confirm"):
            # send message to server with exercise hours and overthinking score as parameters
            commando: str = "Headache by exercise hours and overthinking"
            data: dict = {"exercise_hours": exercise_hours, "overthinking_score": overthinking_score}
            send_message(commando, data)
            response = get_response()

            df = pd.DataFrame(response["dataframe"])
            mode_values = response["mode_values"]
        
        # white space
        st.container(border=False, height=20)

        st.write("##### Result:")
        if st.session_state.confirm and not df.empty:
            with st.container(border=True, height=100):
                st.markdown(f"Common headache frequency: **:primary-background[{mode_values}]**")
        else:
            st.container(border=True, height=100)
    
    with col2:
        # vertical line to separate the columns
        st.markdown(
            """
            <div style="height: 350px; width: 1px; background-color: #5D848D; margin: auto; opacity: 40%;"></div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.container(border=False, height=24)
        if st.session_state.confirm and not df.empty:
            st.bar_chart(df.set_index("Headache_Frequency"), x_label="Headache frequency", y_label="Amount of people", color="#5D848D")
        elif st.session_state.confirm and df.empty:
            st.warning("No dataframe found for the given parameters.", icon="⚠️")