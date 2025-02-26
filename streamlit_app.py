import streamlit as st
import random

st.title("S402 Simulator")

Data=["Smart","Aura","Gyat","Fatty","Stupid","Sigma","This Question Is So Stupid","Shut up","No One Asked"]
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
    
    index=random.randint(1,len(Data))
    bot_response = Data[index-1]
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
