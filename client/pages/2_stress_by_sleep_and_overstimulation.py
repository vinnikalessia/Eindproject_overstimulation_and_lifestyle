# Imports                             |
# ────────────────────────────────────
from communication import check_server_connection, get_server_handler
from connection.connection import ServerHandler
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Average stress level based on sleep and overstimulated", page_icon="🫨", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

check_server_connection()
server_handler = get_server_handler()

# Authentication & app                |
# ────────────────────────────────────
# What is the average stress level of people with the chosen sleep hours and overstimulated?
if not server_handler.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.error("Sorry, you can't use the app unless you are connected and logged in.", icon="❗")
    time.sleep(3)
    st.switch_page("home.py")
else:
    st.markdown(f"## How :primary-background[stressed] are people depending on how much they :primary-background[sleep] and whether they’re :primary-background[overstimulated]?")
    
    # some white space
    st.container(border=False, height=16)

    col1, col2, col3 = st.columns([2.5, 1, 5])

    with col1:
        coli1, coli2 = st.columns(2)
        with coli1:
            sleep_hours = st.number_input("Hours of sleep", min_value=3, max_value=10, value=3, key="sleephours")
        with coli2:
            overstimulated = st.selectbox("Overstimulated?", ["Yes", "No"], key="overstimulated")

        if st.button("Confirm", key="confirm"):
            # send message to server with sleep hours and overstimulated as parameters
            commando: str = "stress by sleep and overstimulated"
            data: dict = {"sleep_hours": sleep_hours, "overstimulated": overstimulated}
            server_handler.send_message(commando, data)
            response = server_handler.get_response(commando)

            df = pd.DataFrame(response["dataframe"])
            mode_values = response["mode_values"]

        # white space
        st.container(border=False, height=20)

        st.write("##### Result:")
        if st.session_state.confirm and not df.empty:
            st.metric(label="Average stress level", value=mode_values, border=True)    
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
            st.bar_chart(df.set_index("Stress_Level"), x_label="Stress level", y_label="Amount of people", color="#5D848D")
        elif st.session_state.confirm and df.empty:
            st.warning("No dataframe found for the given parameters.", icon="⚠️")
