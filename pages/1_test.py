# Imports                             |
# ────────────────────────────────────
from auth import authentication
import streamlit as st
import time

# Setup & init                        |
# ────────────────────────────────────
Auth = authentication.Auth()

user = st.experimental_user
allowed_users = Auth.load_users()

# Authentication & app                |
# ────────────────────────────────────
if not user.is_logged_in:
    Auth.redirecting()
else:
    with st.sidebar:
        st.button("Log out", on_click=st.logout)

    st.text(f"Welcome, {user.name or user.email}!")
    st.text("this is the test page")