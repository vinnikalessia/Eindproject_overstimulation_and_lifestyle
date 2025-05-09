# Imports                             |
# ────────────────────────────────────
import streamlit as st
import json

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Queries", page_icon="❓", layout="wide")

# App                                 |
# ────────────────────────────────────
st.title("Search queries 🔍")

# read the queries.json file
with open("./queries.json", "r", encoding="utf-8") as f:
    queries: list[dict] = json.load(f)

# Find the highest value
max_value = max(queries.values())

# write each query and it's value
for key, value in queries.items():
    if value == max_value and max_value != 0:
        st.metric(label=f":green[{key}] ⬅️ popular query", value=value, delta_color="normal", border=True)
    else:
        st.metric(label=f"**{key}**", value=value, border=True)