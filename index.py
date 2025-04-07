# import streamlit as st

# pages = {
#     "Login": [
#         st.Page("pages/login.py", title="Login"),
#         st.Page("pages/test.py", title="Test"),
#     ]
# }

# pg = st.navigation(pages)
# pg.run()

# if not st.experimental_user.is_logged_in:
#     if st.button("Log in"):
#         st.login()
# else:
#     if st.button("Log out"):
#         st.logout()
#     st.write(f"Hello, {st.experimental_user.name}!")


import streamlit as st
import json
import os

ALLOWED_USERS_FILE = "allowed_users.json"

def load_users():
    if os.path.exists(ALLOWED_USERS_FILE):
        with open(ALLOWED_USERS_FILE) as f:
            return set(json.load(f))
    return set()

def save_users(users):
    with open(ALLOWED_USERS_FILE, "w") as f:
        json.dump(list(users), f)

user = st.experimental_user
allowed_users = load_users()

if not user.is_logged_in:
    st.button("Log in", on_click=st.login)
else:
    if user.email not in allowed_users:
        st.warning("You're not on the allowed list yet.")
        if st.button("Register Me"):
            allowed_users.add(user.email)
            save_users(allowed_users)
            st.success("You’ve been registered! Refresh the app.")
    else:
        st.success(f"Welcome, {user.name or user.email}!")
        st.button("Log out", on_click=st.logout)
        # App content here
