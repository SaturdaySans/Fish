import streamlit as st
import random

st.title("🐟 Fishing Simulator")

FishData = ["Salmon", "Cod", "Tuna", "Golden Carp", "Ancient Leviathan Scale"]
FishRewards = {
    "Salmon": 5,
    "Cod": 3,
    "Tuna": 8,
    "Golden Carp": 20,
    "Ancient Leviathan Scale": 100
}

def fish():
    fish_index = random.randint(0, len(FishData) - 1)
    return FishData[fish_index]

def handle_command(command):
    command = command.strip().lower()

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Cast your rod via command\n"
            "- `/money` — Check thy treasure hoard 💰\n"
            "- `/help` — Display this divine message again"
        )

    elif command == "/fish":
        catch = fish()
        reward = FishRewards.get(catch, 0)
        st.session_state.money += reward
        return f"You cast your line and caught a **{catch}**! 💰 +{reward} Fincoins!"

    elif command == "/money":
        return f"Thy current treasury holds **{st.session_state.money} Fincoins**. 💰"

    else:
        return "Unknown command. Type `/help` for guidance from above."

# 🏦 Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "money" not in st.session_state:
    st.session_state.money = 0

# 📜 Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✉️ Handle slash command input
if prompt := st.chat_input("Enter a command like /fish or /money"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = handle_command(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
