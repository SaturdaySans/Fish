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
            "- `/money` — Check your fortune 💰\n"
            "- `/help` — Reveal the secrets of the abyss"
        )

    elif command == "/fish":
        catch = fish()
        reward = FishRewards.get(catch, 0)
        st.session_state.money += reward
        return f"You cast your line and caught a **{catch}**! 💰 +{reward} Fincoins!"

    elif command == "/money":
        return f"Thy current treasury holds **{st.session_state.money} Fincoins**. 💰"

    else:
        return "Unknown command. Type `/help` to see what thou canst do."

# 🏦 Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "money" not in st.session_state:
    st.session_state.money = 0

# 💬 Display all past messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
    # Add button only after the **last assistant message**
    if i == len(st.session_state.messages) - 1 and message["role"] == "assistant":
        if st.button("🎣 Fish Again", key=f"fish_button_{i}"):
            catch = fish()
            reward = FishRewards.get(catch, 0)
            st.session_state.money += reward

            user_msg = "🎣 Rod Casted"
            response = f"You boldly press the divine button... and behold! A **{catch}** is caught! 💰 +{reward} Fincoins!"

            with st.chat_message("user"):
                st.markdown(user_msg)

            with st.chat_message("assistant"):
                st.markdown(response)

            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.experimental_rerun()  # Refresh immediately to insert button after new message

# 👂 Handle chat input
if prompt := st.chat_input("Enter a command:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    bot_response = handle_command(prompt)

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
