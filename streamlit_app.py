import streamlit as st
import random

st.title("🐟 Fishing Simulator")

# 🎏 The Vast Pool of Fontaine's Finned Folk
FishPool = [
    {"name": "Salmon", "rarity": "Common", "weight": 50, "reward": 5},
    {"name": "Cod", "rarity": "Common", "weight": 50, "reward": 3},
    {"name": "Mackerel", "rarity": "Common", "weight": 40, "reward": 4},
    {"name": "Anchovy", "rarity": "Common", "weight": 45, "reward": 2},
    {"name": "Herring", "rarity": "Common", "weight": 40, "reward": 3},
    {"name": "Tuna", "rarity": "Uncommon", "weight": 20, "reward": 8},
    {"name": "Sardine Swarm", "rarity": "Uncommon", "weight": 20, "reward": 7},
    {"name": "Sea Bass", "rarity": "Uncommon", "weight": 18, "reward": 9},
    {"name": "Golden Carp", "rarity": "Rare", "weight": 10, "reward": 20},
    {"name": "Electric Eel", "rarity": "Rare", "weight": 10, "reward": 22},
    {"name": "Moon Jellyfish", "rarity": "Rare", "weight": 8, "reward": 18},
    {"name": "Swordfish", "rarity": "Epic", "weight": 5, "reward": 40},
    {"name": "Ornamental Koi", "rarity": "Epic", "weight": 4, "reward": 35},
    {"name": "Crystal Lionfish", "rarity": "Epic", "weight": 3, "reward": 50},
    {"name": "Ancient Leviathan Scale", "rarity": "Legendary", "weight": 1, "reward": 100},
    {"name": "Abyssal Kraken Tentacle", "rarity": "Legendary", "weight": 1, "reward": 120},
    {"name": "Phantom Seahorse", "rarity": "Legendary", "weight": 1, "reward": 90},
    {"name": "Mythic Coral Wyrm", "rarity": "Legendary", "weight": 1, "reward": 150},
    {"name": "Celestial Bubblefish", "rarity": "Legendary", "weight": 1, "reward": 130},
]

# 🎣 Weighted Random Fish
def fish():
    names = [f["name"] for f in FishPool]
    weights = [f["weight"] for f in FishPool]
    chosen_name = random.choices(names, weights=weights, k=1)[0]
    return next(f for f in FishPool if f["name"] == chosen_name)

# 🧾 Command Handler
def handle_command(command):
    command = command.strip().lower()

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Cast thy rod and tempt the deep\n"
            "- `/inventory` — Examine thy glorious catches 🧺\n"
            "- `/sell` — Sell all thy fish for Fincoins 💰\n"
            "- `/money` — View thy coinage 💰\n"
            "- `/experience` — Behold thy accumulated wisdom ✨\n"
            "- `/shop` — View fish sell values 📜\n"
            "- `/help` — This guide of holy waters"
        )

    elif command == "/fish":
        catch = fish()
        st.session_state.experience += 1

        # Update Inventory
        name = catch["name"]
        if name in st.session_state.inventory:
            st.session_state.inventory[name]["count"] += 1
        else:
            st.session_state.inventory[name] = {"rarity": catch["rarity"], "count": 1}

        return (
            f"You cast your rod... and lo! You caught a **{catch['rarity']} {name}**! 🐟\n"
            f"✨ +1 XP\n"
            f"(Sell it later using `/sell` to earn Fincoins!)"
        )

    elif command == "/money":
        return f"Thy treasury holdeth **{st.session_state.money} Fincoins**. 💰"

    elif command == "/experience":
        return f"Thou hast earned **{st.session_state.experience} XP** through fishful valor. ✨"

    elif command == "/inventory":
        if not st.session_state.inventory:
            return "Thy basket is empty. Go forth and fish!"
        response = "**Inventory of Caught Creatures:**\n"
        for name, info in st.session_state.inventory.items():
            response += f"- **{info['rarity']} {name}** × {info['count']}\n"
        return response

    elif command == "/sell":
        if not st.session_state.inventory:
            return "Thou possesseth no fish to sell, o poor soul!"

        total_earned = 0
        summary = "**You step into the market and sell thy bounty:**\n"

        for name, info in st.session_state.inventory.items():
            count = info["count"]
            fish_data = next(f for f in FishPool if f["name"] == name)
            reward = fish_data["reward"]
            earned = reward * count
            total_earned += earned
            summary += f"- **{info['rarity']} {name}** × {count} → 💰 +{earned} Fincoins\n"

        st.session_state.money += total_earned
        st.session_state.inventory = {}  # Clear inventory

        summary += f"\n💰 **Total Earned:** {total_earned} Fincoins!"
        return summary

    elif command == "/shop":
        response = "**📜 Fish Shop — Current Sell Values:**\n"
        for fish in FishPool:
            response += f"- **{fish['rarity']} {fish['name']}** → {fish['reward']} Fincoins\n"
        return response

    else:
        return "Unknown command. Use `/help` to consult the waves of wisdom."


# 🌊 State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "money" not in st.session_state:
    st.session_state.money = 0

if "experience" not in st.session_state:
    st.session_state.experience = 0

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

# 📜 Show Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💬 Process Command Input
if prompt := st.chat_input("Type /fish, /inventory, /experience, etc."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = handle_command(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
