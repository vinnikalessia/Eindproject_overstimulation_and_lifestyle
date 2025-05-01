from connection.connection import ServerHandler
from dotenv import load_dotenv
import streamlit as st
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
        # will execute the run function
        server_handler.start()
        st.session_state.connected = True
        st.session_state.state_message = "You are succesfully connected!"
        return server_handler
    except socket.error as e:
        st.session_state.state_message = f"Connection error: {e}. Please check your connection and try again."
        time.sleep(3)
        return None
    except Exception as e:
        st.session_state.state_message = f"An error occurred: {e}. Please try again later."
        time.sleep(3)
        return None

# check if the connection is still alive
@st.fragment(run_every=3)
def check_server_connection():
    if st.session_state.connected:
        server_handler = get_server_handler()
        
        # check connection with server
        try:
            server_handler.send_message("ping", {})
        except Exception as e:
            st.session_state.connected = False
            server_handler.io_stream.close()
            server_handler.socket_to_server.close()
            st.toast(f"Connection error: {e}. Please check your connection and try again.", icon="❗")
            time.sleep(1)
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
    else:
        print("Not connected to the server.")