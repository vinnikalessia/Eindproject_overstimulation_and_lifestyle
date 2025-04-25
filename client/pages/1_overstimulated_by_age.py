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
st.set_page_config(page_title="Overstimulated by age", page_icon="😥", layout="wide")

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
# How many people are overstimulated with the chosen age?
if not st.session_state.connected or not st.session_state.user:
    st.title("Welcome guest! 👋")
    st.error("Sorry, you can't use the app unless you are connected and logged in.", icon="❗")
    time.sleep(3)
    st.switch_page("home.py")
else:
    # st.markdown("## How many people are :primary-background[overstimulated] in the selected :primary-background[age] group?")
    st.markdown("## What is the number of individuals who are :primary-background[overstimulated] in the chosen :primary-background[age] category?")


    # some white space
    st.container(border=False, height=32)

    col1, col2, col3 = st.columns([2.5, 1, 5])

    with col1:
        input_age = st.number_input("Select an age", min_value=18, max_value=100, value=18)

        if st.button("Confirm", key="confirm"):
            # send message to server with age as parameter
            age = input_age
            msg: dict = {"commando": "Overstimulated by age", "Age": age}
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
                # Replace 0/1 with No/Yes
                data["Overstimulated"] = data["Overstimulated"].replace({0: "No", 1: "Yes"})

                # Count how many people are overstimulated or not
                counts = data["Overstimulated"].value_counts().reset_index()
                counts.columns = ["Overstimulated", "Count"]

                # plot the data in other column for more beautiful view
        
        # white space
        st.container(border=False, height=20)

        st.write("##### Result:")
        if st.session_state.confirm and not data.empty:
            with st.container(border=True, height=100):
                st.write(f"**:primary-background[{res['overstimulated']}]** out of **:primary-background[{res['total']}]** people are overstimulated at age **:primary-background[{age}]**.")
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
            st.bar_chart(counts.set_index("Overstimulated"), x_label="Overstimulated or not", y_label="Amount of people", color="#5D848D")
        elif st.session_state.confirm and data.empty:
            st.warning("No data found for the given parameters.", icon="⚠️")
