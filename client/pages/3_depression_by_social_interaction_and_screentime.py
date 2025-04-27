# Imports                             |
# ────────────────────────────────────
from communication import send_message, check_server_connection, get_response
from connection.connection import ClientServerConnection
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Average depression score based on social interaction and screen time", page_icon="😟", layout="wide")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "user" not in st.session_state:
    st.session_state.user = None

check_server_connection()

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
    
    # some white space
    st.container(border=False, height=16)

    col1, col2, col3 = st.columns([2.5, 1, 5])

    with col1:
        coli1, coli2 = st.columns(2)
        with coli1:
            social_interaction = st.number_input("Social interaction", min_value=0, max_value=9, value=0, help="How many :primary-badge[times] there is a social interaction in a day.", key="social_interactions")
        with coli2:
            screen_time = st.number_input("Screen time", min_value=0, max_value=12, value=0, help="Rounded by :primary-badge[hours]", key="screentime")
        
        if st.button("Confirm", key="confirm"):
            # send message to server with social interactions and screen time as parameters
            commando: str = "Depression by social interactions and screen time"
            data: dict = {"social_interaction": social_interaction, "screen_time": screen_time}
            send_message(commando, data)
            response = get_response()

            df = pd.DataFrame(response["dataframe"])
            mode_values = response["mode_values"]

        # white space
        st.container(border=False, height=20)

        st.write("##### Result:")
        if st.session_state.confirm and not df.empty:
            with st.container(border=True, height=100):
                st.markdown(f"Common depression score: **:primary-background[{mode_values}]**")
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
            st.bar_chart(df.set_index("Depression_Score"), x_label="Depression score", y_label="Amount of people", color="#5D848D")
        elif st.session_state.confirm and df.empty:
            st.warning("No dataframe found for the given parameters.", icon="⚠️")