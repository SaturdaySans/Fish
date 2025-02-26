import streamlit as st

st.title("💬 Simple Chatbot")

# Create a session state variable to store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("Say something:"):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Predetermined chatbot response
    bot_response = "hi"
    
    # Display chatbot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Store chatbot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
