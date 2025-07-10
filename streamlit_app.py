import streamlit as st
import random

st.title("Fishing Simulator")

FishData = ["Salmon", "Cod"]

def fish():
    fish_index = random.randint(0, len(FishData) - 1)
    return FishData[fish_index]

class_list = ["a", "b", "c"]  # Alas, unused still, but preserved for future tales...

# Session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Say something:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # The divine catch of the day!
    bot_response = fish()
    
    with st.chat_message("assistant"):
        st.markdown(f"You caught a **{bot_response}**! 🎣")
    
    st.session_state.messages.append({"role": "assistant", "content": f"You caught a **{bot_response}**! 🎣"})
