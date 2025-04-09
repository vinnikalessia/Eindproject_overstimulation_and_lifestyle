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
    st.title("Hello guest! 👋")
    st.markdown("#### ⬅️ To use this app, please log in.")
    with st.sidebar:
        st.button("Log in", on_click=st.login)
else:
    with st.sidebar:
        st.button("Log out", on_click=st.logout)

    if user.email not in allowed_users:
        allowed_users.add(user.email)
        Auth.save_users(allowed_users)
        st.success("You’ve been registered! Changes are being saved...")
        time.sleep(3)
        st.rerun()
    else:
        st.text(f"Welcome, {user.name or user.email}!")

