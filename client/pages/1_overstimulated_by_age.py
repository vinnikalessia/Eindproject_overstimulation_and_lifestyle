# Imports                             |
# ────────────────────────────────────
from communication import send_message, check_server_connection, get_response
from connection.connection import ServerHandler
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import time
import json
import os

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Overstimulated by age", page_icon="😥", layout="wide")

if "connected" not in st.session_state:
    st.session_state.connected = False

if "user" not in st.session_state:
    st.session_state.user = None

check_server_connection()

# Authentication & app                |
# ────────────────────────────────────
# How many people are overstimulated with the chosen age?
if not st.session_state.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.error("Sorry, you can't use the app unless you are connected and logged in.", icon="❗")
    time.sleep(3)
    st.switch_page("home.py")
else:
    st.markdown("## What is the number of individuals who are :primary-background[overstimulated] in the chosen :primary-background[age] category?")

    # some white space
    st.container(border=False, height=16)

    col1, col2, col3 = st.columns([2.5, 1, 5])

    with col1:
        age = st.number_input("Select an age", min_value=18, max_value=100, value=18)

        if st.button("Confirm", key="confirm"):
            # send message to server with age as parameter
            commando: str = "overstimulated by age"
            data: dict = {"age": age}
            send_message(commando, data)
            response = get_response(commando)

            total = response["total"]
            overstimulated = response["overstimulated"]
            df_dict: dict = response["dataframe"]
            df = pd.DataFrame(df_dict)

        # white space
        st.container(border=False, height=20)

        st.write("##### Result:")
        if st.session_state.confirm and not df.empty:
            st.metric(label="Overstimulated", value=overstimulated, border=True)
        else:
            st.container(border=True, height=105)

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
            st.bar_chart(df.set_index("Overstimulated"), x_label="Overstimulated or not", y_label="Amount of people", color="#5D848D")
        elif st.session_state.confirm and df.empty:
            st.warning("No dataframe found for the given parameters.", icon="⚠️")
