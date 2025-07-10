import streamlit as st
import random

st.title("🐟 Fishing Simulator - Slash & Button Edition")

FishData = ["Salmon", "Cod", "Tuna", "Golden Carp", "Ancient Leviathan Scale"]

def fish():
    fish_index = random.randint(0, len(FishData) - 1)
    return FishData[fish_index]

def handle_command(command):
    command = command.strip().lower()

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Try your luck and catch a fish!\n"
            "- `/help` — Show this help message."
        )
    elif command == "/fish":
        catch = fish()
        return f"You cast your line into the watery abyss... and caught a **{catch}**! 🎣"
    else:
        return "Unknown command. Type `/help` to see what you can do."

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💬 Handle chat input
if prompt := st.chat_input("Enter a command like /fish or /help"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    bot_response = handle_command(prompt)

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# 🎣 The Divine Button of Destiny
if st.button("🎣 Fish Now"):
    catch = fish()
    response = f"You boldly press the divine button... and behold! A **{catch}** is caught! 🌊✨"
    
    with st.chat_message("user"):
        st.markdown("🎣 [Button Pressed] Fish Now")

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "user", "content": "🎣 [Button Pressed] Fish Now"})
    st.session_state.messages.append({"role": "assistant", "content": response})
