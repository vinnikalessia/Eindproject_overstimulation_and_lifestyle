# Imports                             |
# ────────────────────────────────────
from server import Server
import streamlit as st

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Homepage", page_icon="🏠")

# if "clients" not in st.session_state:
#     st.session_state.clients = None

@st.cache_resource(show_spinner=False)
def run_server():
    """
    Establish a connection to the server.
    """
    server = Server()
    server.start()
    return server

server = run_server()

st.title(f"Welcome to the :primary-background[server]! 👋")

# list_users = server.get_users()
# st.write(list_users)



