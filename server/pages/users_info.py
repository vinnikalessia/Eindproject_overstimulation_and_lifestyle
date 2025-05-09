# Imports                             |
# ────────────────────────────────────
import streamlit as st
import json

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Users info", page_icon="🙂", layout="wide")

# App                                 |
# ────────────────────────────────────
st.title("Users info 🙂")

# read the users.json file
with open("./users.json", "r", encoding="utf-8") as f:
    users: list[dict] = json.load(f)

# write each user and it's value
for user in users:
    with st.expander(f"**User: {user['name']}**", expanded=False):
        # get all the queries of the user
        query = user["overstimulated by age"]
        st.metric(label="overstimulated by age", value=query, delta_color="normal", border=True)
        
        query = user["stress by sleep and overstimulated"]
        st.metric(label="stress by sleep and overstimulated", value=query, delta_color="normal", border=True)
        
        query = user["depression by social interactions and screen time"]
        st.metric(label="depression by social interactions and screen time", value=query, delta_color="normal", border=True)
        
        query = user["headache by exercise hours and overthinking"]
        st.metric(label="headache by exercise hours and overthinking", value=query, delta_color="normal", border=True)