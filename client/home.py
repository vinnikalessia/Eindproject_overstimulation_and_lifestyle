# Imports                             |
# ────────────────────────────────────
from communication import get_server_handler, check_server_connection
import streamlit as st
import time

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Homepage", page_icon="🏠")

if "user" not in st.session_state:
    st.session_state.user = ""

server_handler = get_server_handler()
check_server_connection()

def connect_button():
    col1, col2 = st.columns([3, 4])
    with col1:
        if server_handler.connected == True:
            if st.button(":red[:material/wifi_off:] Disconnect from server"):
                with st.spinner("Disconnecting..."):
                    time.sleep(1)
                    server_handler.close()
                    st.session_state.user = ""
                    st.cache_resource.clear()
                    st.rerun()

        else:
            if st.button(":green[:material/wifi:] Connect to server"):
                with st.spinner("Connecting..."):
                    server_handler.start()
                    time.sleep(2)
                    st.rerun()
    with col2:
        if server_handler.connected:
            st.success("You are succesfully connected!", icon="✅")
        else:
            st.error("You are not connected.", icon="❗")

# Authentication & app                |
# ────────────────────────────────────
if not server_handler.connected or st.session_state.user == "":
    st.title("Welcome guest! 👋")
    st.markdown("#### To use this app, please connect to the server first and login.")
else:
    st.title(f"Welcome back! {st.session_state.user} 👋")

connect_button()

if st.session_state.user == "":
    # input fields for login
    name = st.text_input(":material/person: Enter your name", key="name", disabled=not server_handler.connected)
    password = st.text_input(":material/key: Enter your password", key="password", type="password", disabled=not server_handler.connected)

    disabled = not server_handler.connected or not name or not password
    help = "Please connect to the server first." if not server_handler.connected else ""
    help = "Enter all fields" if not name or not password else help

    if st.button("Login", type="primary", disabled=disabled, help=help):
        if name and password:
            # Send the login data to the server
            with st.spinner("Logging in..."):
                time.sleep(1)
                commando = "login"
                data = {"name": name, "password": password}
                server_handler = get_server_handler()
                server_handler.send_message(commando, data)
                response = server_handler.get_response(commando)
                st.write(f"Server response: {response}")

            if response == "Success":
                st.session_state.user = name
                st.success(f"Login successful!")
                st.rerun()
            else:
                st.error("Login failed. Please try again.")
        else:
            st.warning("Please enter both name and password.")
else:
    st.write(st.session_state.user)
    st.write("You are logged in.")
