import streamlit as st
import random

st.title("Fishing Simulator")

FishData=["Salmon", "Cod"]

def fish():
    Fish_Index = random.randint(0,len(FishData))
    return FishData[Fish_Index]

Class_List = ["a","b","c"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    bot_response = fish()
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
