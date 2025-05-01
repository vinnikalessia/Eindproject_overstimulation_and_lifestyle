# Imports                             |
# ────────────────────────────────────
from server import ClientHandler
from server import Server
import streamlit as st
import time

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Homepage", page_icon="🏠")

def show_avatar(image_url, name, caption):
    html_content = f"""
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <img src="{image_url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 50%; margin-right: 15px;" />
            <div style="display: flex; flex-direction: column;">
                <span style="font-weight: bold; font-size: 18px; color: #1c1c1c;">{name}</span>
                <span style="color: gray; font-size: 14px;">{caption}</span>
            </div>
        </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

@st.fragment(run_every=3)
def rerunner():
    """
    Rerun the Streamlit app every 3 seconds.
    """

    for client_handler in server.clienthandlers:
        name = client_handler.name if client_handler.name != "" else "Guest"
        col1, col2, col3 = st.columns(3, vertical_alignment="center")
        with col1:
            show_avatar(
                "https://media.discordapp.net/attachments/1175112305067962388/1367170502941999164/image.png?ex=68144500&is=6812f380&hm=91173afd7800fa376a6bbfee85c11b9e8d3fb8a33899d598d325290f8f9e28d0&format=webp&quality=lossless&width=283&height=259&",
                name,
                f"{client_handler.addr[0]}:{client_handler.addr[1]}",
            )
        with col2:
            if st.button("Send message", key=f"send_message_{client_handler.addr[1]}"):
                res = server.send_message_to_client(client_handler.name, f"Hello {client_handler.name}!")
                if res:
                    st.toast("Message sent successfully!", icon="✅")
                else:
                    st.toast(":red[Failed to send message. Client not found.]", icon="❗")
        with col3:
            if st.button("Disconnect", key=f"disconnect_{client_handler.addr[1]}"):
                res = client_handler.close()
                if res:
                    st.toast("Client disconnected successfully!", icon="✅")
                else:
                    st.toast(":red[Failed to disconnect client. Client not found.]", icon="❗")
                time.sleep(1)
                st.rerun()

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

rerunner()