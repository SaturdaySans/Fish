import streamlit as st
import random

st.title("🐟 Fishing Simulator — Rarity Edition")

# 🐟 Fish Pool with Rarities
FishPool = [
    # 🟢 Common (Reward: 2–6)
    {"name": "Salmon", "rarity": "Common", "weight": 40, "reward": 5},
    {"name": "Cod", "rarity": "Common", "weight": 40, "reward": 3},
    {"name": "Mackerel", "rarity": "Common", "weight": 30, "reward": 4},
    {"name": "Anchovy", "rarity": "Common", "weight": 35, "reward": 2},
    {"name": "Herring", "rarity": "Common", "weight": 30, "reward": 3},

    # 🔵 Uncommon (Reward: 7–10)
    {"name": "Tuna", "rarity": "Uncommon", "weight": 20, "reward": 8},
    {"name": "Sardine Swarm", "rarity": "Uncommon", "weight": 20, "reward": 7},
    {"name": "Sea Bass", "rarity": "Uncommon", "weight": 18, "reward": 9},

    # 🟣 Rare (Reward: 15–25)
    {"name": "Golden Carp", "rarity": "Rare", "weight": 10, "reward": 20},
    {"name": "Electric Eel", "rarity": "Rare", "weight": 10, "reward": 22},
    {"name": "Moon Jellyfish", "rarity": "Rare", "weight": 9, "reward": 18},

    # 🔶 Epic (Reward: 30–60)
    {"name": "Swordfish", "rarity": "Epic", "weight": 5, "reward": 40},
    {"name": "Ornamental Koi", "rarity": "Epic", "weight": 4, "reward": 35},
    {"name": "Crystal Lionfish", "rarity": "Epic", "weight": 3, "reward": 50},

    # 🔴 Legendary (Reward: 80–150)
    {"name": "Ancient Leviathan Scale", "rarity": "Legendary", "weight": 1, "reward": 100},
    {"name": "Abyssal Kraken Tentacle", "rarity": "Legendary", "weight": 1, "reward": 120},
    {"name": "Phantom Seahorse", "rarity": "Legendary", "weight": 1, "reward": 90},
    {"name": "Mythic Coral Wyrm", "rarity": "Legendary", "weight": 1, "reward": 150},
    {"name": "Celestial Bubblefish", "rarity": "Legendary", "weight": 1, "reward": 130},
]


# 🎣 Summoneth a fish based on weighted rarity
def fish():
    names = [f["name"] for f in FishPool]
    weights = [f["weight"] for f in FishPool]
    chosen_name = random.choices(names, weights=weights, k=1)[0]
    chosen_fish = next(f for f in FishPool if f["name"] == chosen_name)
    return chosen_fish

# 🧾 Command Handler
def handle_command(command):
    command = command.strip().lower()

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Cast thy line and tempt the depths\n"
            "- `/money` — Count thy glimmering coins\n"
            "- `/help` — This divine guidance"
        )

    elif command == "/fish":
        catch = fish()
        st.session_state.money += catch["reward"]
        return (
            f"You cast your rod... and lo! You caught a **{catch['rarity']} {catch['name']}**! 🐟\n"
            f"💰 +{catch['reward']} Fincoins!"
        )

    elif command == "/money":
        return f"Thy treasury overfloweth with **{st.session_state.money} Fincoins**. 💰"

    else:
        return "Unknown command. Use `/help` if thou art lost in the currents of confusion."

# 🏦 Initialize State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "money" not in st.session_state:
    st.session_state.money = 0

# 📜 Display Past Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💬 Handle Commands
if prompt := st.chat_input("Type /fish, /money or /help"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = handle_command(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
