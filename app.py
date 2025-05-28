import streamlit as st
import requests
import datetime

st.set_page_config(page_title="AI Career Counsellor", page_icon="🎯")

st.title("🎯 AI Virtual Career Counsellor")
st.markdown("Ask me about your career interests and I'll recommend a suitable career path!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def save_chat_history():
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        for msg in st.session_state.messages:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg['sender'].upper()}: {msg['text']}\n")
        f.write("\n--- New Session ---\n\n")

def send_message(message):
    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"message": message},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return [{"text": "Sorry, I'm having trouble connecting to the server."}]

# Input area and buttons in a form to allow "Enter" to send
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submit_button = st.form_submit_button(label="Send")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

if submit_button and user_input:
    st.session_state.messages.append({"sender": "user", "text": user_input})

    with st.spinner("Waiting for response..."):
        bot_responses = send_message(user_input)

    for resp in bot_responses:
        st.session_state.messages.append({"sender": "bot", "text": resp.get("text")})

    save_chat_history()

# Display chat messages with simple chat bubble styling
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#DCF8C6;
                padding:10px;
                border-radius:10px;
                max-width:70%;
                margin-left:auto;
                margin-bottom:5px;
                ">
                <b>You:</b> {msg['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#F1F0F0;
                padding:10px;
                border-radius:10px;
                max-width:70%;
                margin-right:auto;
                margin-bottom:5px;
                ">
                <b>Bot:</b> {msg['text']}
            </div>
            """,
            unsafe_allow_html=True,
        )
