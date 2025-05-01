from connection.connection import ServerHandler
from dotenv import load_dotenv
import streamlit as st
import logging
import socket
import time
import os

@st.cache_resource(show_spinner=False)
def get_server_handler():
    try:
        load_dotenv()
        host = os.getenv("HOST")
        port = int(os.getenv("PORT"))
        server_handler = ServerHandler(host, port)
        return server_handler
    except Exception as e:
        st.toast(f"An error occurred: {e}. Please check your connection and try again.", icon="❗")
        time.sleep(3)
        return None


# check if the connection is still alive
@st.fragment(run_every=3)
def check_server_connection():
    server_handler = get_server_handler()
    print(f"connected: {server_handler.connected}")
    print(f"terminated: {server_handler.terminated}")

    if server_handler.connected:
        # check connection with server
        try:
            server_handler.send_message("ping", {})
        except Exception as e:
            server_handler.connected = False
            st.session_state.user = ""
            server_handler.io_stream.close()
            server_handler.socket_to_server.close()
            st.cache_resource.clear()
            st.toast(f"Connection error: {e}. Please check your connection and try again.", icon="❗")
            time.sleep(3)
            st.rerun(scope="app")
            return

        message_from_server = None
        if server_handler.received_messages:
            for msg in server_handler.received_messages:
                if msg["commando"] == "message":
                    server_handler.received_messages.remove(msg)
                    message_from_server = msg["data"]
                    break
        if message_from_server:
            st.toast(f"Server message: {message_from_server}", icon="📬")
            time.sleep(3)
    elif server_handler.terminated:
        print("Not connected to the server.")

        # check if the thread was started already
        st.session_state.user = ""
        st.cache_resource.clear()
        st.toast(f"Server has terminated your connection or something went wrong.", icon="⚠️")
        time.sleep(3)
        st.rerun(scope="app")