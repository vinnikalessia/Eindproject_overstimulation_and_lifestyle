# Imports                             |
# ────────────────────────────────────
import streamlit as st
import json
import time
import os

# Setup & init                        |
# ────────────────────────────────────
ALLOWED_USERS_FILE = "./allowed_users.json"

# Authentication class                |
# ────────────────────────────────────
class Auth():
    @staticmethod
    def load_users():
        if os.path.exists(ALLOWED_USERS_FILE):
            with open(ALLOWED_USERS_FILE) as f:
                return set(json.load(f))
        return set()

    @staticmethod
    def save_users(users):
        with open(ALLOWED_USERS_FILE, "w") as f:
            json.dump(list(users), f)
    
    @staticmethod
    def redirecting():
        st.error("You should be logged in to see this page.", icon="❗")
        with st.spinner("Redirecting soon...", show_time=False):
            time.sleep(3)
        st.switch_page("home.py")
