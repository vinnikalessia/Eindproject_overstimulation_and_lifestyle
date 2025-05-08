# Imports                             |
# ────────────────────────────────────
from server import Server
import streamlit as st
import time

# Setup & init                        |
# ────────────────────────────────────
st.set_page_config(page_title="Server", page_icon="🗄️", layout="wide")

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

@st.fragment(run_every=3)
def logging_file(debug_level="ALL"):
    log_file = "./logging/server.log"
    with open(log_file, "r") as f:
        log_lines = f.readlines()

    # take only the last 10 lines of the level debug_level and reverse their order
    if debug_level == "ALL":
        last_10_logs = log_lines[-10:][::-1]
    else:
        last_10_logs = [line for line in log_lines if debug_level in line][-10:][::-1]
    
    for line in last_10_logs:
        if "INFO" in line:
            st.info(line.strip())
        elif "WARNING" in line:
            st.warning(line.strip())
        elif "ERROR" in line:
            st.error(line.strip())
        else:
            st.write(line.strip())

@st.cache_resource(show_spinner=False)
def run_server():
    """
    Establish a connection to the server.
    """
    server = Server()
    server.start()
    return server

server = run_server()

colt1, colt2, colt3 = st.columns([2, 2.8, 2])
with colt2:
    st.title("Welcome to the :primary-background[server]! 👋")

st.container(border=False, height=16)

col1, col2, col3 = st.columns([5, 1, 5])
with col1:
    st.write("### Connected Clients")
    rerunner()
    
with col2:
    # vertical line to separate the columns
    st.markdown(
        """
        <div style="height: 400px; width: 1px; background-color: #5D848D; margin: auto; opacity: 40%;"></div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown("### Logging", help="This is the logging of the server. You can see the :primary-background[last 10 messages] of :primary-background[each level].")

    tab1, tab2, tab3, tab4 = st.tabs(["**:primary[all]**", "**:blue[info]**", "**:orange[warning]**", "**:red[error]**"])

    with tab1:
        logging_file()
    with tab2:
        logging_file("INFO")
    with tab3:
        logging_file("WARNING")
    with tab4:
        logging_file("ERROR")

