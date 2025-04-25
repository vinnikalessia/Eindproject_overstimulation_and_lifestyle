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
st.set_page_config(page_title="Average stress level based on sleep and overstimulated", page_icon="🫨", layout="wide")

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
    
    # some white space
    st.container(border=False, height=32)

    col1, col2, col3 = st.columns([2.5, 1, 5])

    with col1:
        coli1, coli2 = st.columns(2)
        with coli1:
            sleep_hours = st.number_input("Hours of sleep", min_value=3, max_value=10, value=3, key="sleephours")
        with coli2:
            overstimulated = st.selectbox("Overstimulated?", ["Yes", "No"], key="overstimulated")

        if st.button("Confirm", key="confirm"):
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

            # check if data is empty
            if not data.empty:
                counts = data["Stress_Level"].value_counts().reset_index()
                counts.columns = ["Stress_Level", "Count"]

            # plot the data in other column for more beautiful view

        # white space
        st.container(border=False, height=20)

        st.write("##### Result:")
        if st.session_state.confirm and not data.empty:
            with st.container(border=True, height=100):
                modes = data['Stress_Level'].mode()
                mode_values = ' and '.join([str(int(val)) if isinstance(val, int) else str(round(val, 2)) for val in modes])

                st.markdown(f"Common stress level: **:primary-background[{mode_values}]**")
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
        st.container(border=False, height=20)
        if st.session_state.confirm and not data.empty:
            st.bar_chart(counts.set_index("Stress_Level"), x_label="Stress level", y_label="Amount of people", color="#5D848D")
        elif st.session_state.confirm and data.empty:
            st.warning("No data found for the given parameters.", icon="⚠️")
