import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

st.title("💬 Gemini Chatbot")

# 1. Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. User input (chat-style)
user_input = st.chat_input("Ask something...")

if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # 4. Send full conversation to Gemini
    conversation = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )

    reply = response.text

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # Display AI response
    with st.chat_message("assistant"):
        st.write(reply)