import streamlit as st
import random

st.title("S402 Simulator")

Data=["Smart","Aura","Ms Deana, We Don't Have Enough Time","Sings","Punches you","Stupid","Sigma","This Question Is So Stupid","Ms Deana Is The Math Test Tommorow"]

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
    bot_response = Data[index]
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
