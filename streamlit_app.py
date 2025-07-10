import streamlit as st
import random
import time
from fish_data import FishPool, BaitEffects

st.title("🐟 Fishing Simulator")



# 🧠 XP to Level Conversion
def get_level_and_progress(experience):
    level = int(experience ** 0.5)
    next_level_xp = (level + 1) ** 2
    current_level_xp = level ** 2
    progress = experience - current_level_xp
    needed = next_level_xp - current_level_xp
    return level, progress, needed

# 🐠 Weighted Fishing Logic
def go_fishing():
    xp = st.session_state.experience
    level, _, _ = get_level_and_progress(xp)
    rod_level = st.session_state.rod_level
    bait = st.session_state.current_bait
    bait_effect = BaitEffects.get(bait, BaitEffects["Worm Bait"])

    adjusted_weights = []
    for f in FishPool:
        rarity = f["rarity"]
        base = f["weight"]
        bonus = rod_level * 0.015
        rarity_bonus = bait_effect[rarity]
        if rarity == "Common":
            adjusted = base * max(1.0 - (level * 0.02 + rod_level * 0.03), 0.1) * rarity_bonus
        else:
            scale = {
                "Uncommon": 0.01,
                "Rare": 0.02,
                "Epic": 0.025,
                "Legendary": 0.03,
                "Mythical": 0.04
            }[rarity]
            adjusted = base * (1.0 + level * scale + bonus) * rarity_bonus
        adjusted_weights.append(adjusted)

    names = [f["name"] for f in FishPool]
    chosen_name = random.choices(names, weights=adjusted_weights, k=1)[0]
    return next(f for f in FishPool if f["name"] == chosen_name)

# 🧾 Command Handler
def handle_command(command):
    command = command.strip().lower()

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Cast thy rod and tempt the deep\n"
            "- `/inventory` — View caught fish 🧺\n"
            "- `/sell` — Sell fish for Fincoins 💰\n"
            "- `/money` — View thy wealth 💰\n"
            "- `/experience` — Check thy fishing level ✨\n"
            "- `/shop` — Upgrade rod / Buy bait / Change bait 🎣\n"
            "- `/help` — This guide of holy waters"
        )

    elif command == "/fish":
        if st.session_state.bait <= 0:
            return "🪱 You have no bait! Visit the `/shop` to buy more."

        catch = go_fishing()
        st.session_state.experience += 1
        st.session_state.bait -= 1

        # 🎬 Delay based on rarity
        rarity = catch["rarity"]
        delay_map = {
            "Common": (0.5, 1.0),
            "Uncommon": (1.0, 1.5),
            "Rare": (1.5, 2.0),
            "Epic": (2.0, 2.5),
            "Legendary": (2.5, 3.0),
            "Mythical": (3.0, 3.5)
        }
        time.sleep(random.uniform(*delay_map[rarity]))

        # 📦 Inventory update
        name = catch["name"]
        if name in st.session_state.inventory:
            st.session_state.inventory[name]["count"] += 1
        else:
            st.session_state.inventory[name] = {"rarity": catch["rarity"], "count": 1}

        return (
            f"You cast your rod... and lo! You caught a **{catch['rarity']} {name}**! 🐟\n"
            f"✨ +1 XP | 🪱 -1 Bait (Remaining: {st.session_state.bait})\n"
            f"(Sell it later using `/sell` to earn Fincoins!)"
        )

    elif command == "/money":
        return f"Thy treasury holdeth **{st.session_state.money} Fincoins**. 💰"

    elif command == "/experience":
        xp = st.session_state.experience
        level, progress, needed = get_level_and_progress(xp)
        st.markdown(f"**Level {level}** — {progress}/{needed} XP to next level ✨")
        st.progress(progress / needed)
        return f"Your fishing prowess grows. You are **Level {level}**, with **{xp} XP**."

    elif command == "/inventory":
        if not st.session_state.inventory:
            return "Thy basket is empty. Go forth and fish!"
        response = "**Inventory of Caught Creatures:**\n"
        for name, info in st.session_state.inventory.items():
            response += f"- **{info['rarity']} {name}** × {info['count']}\n"
        return response

    elif command == "/sell":
        if not st.session_state.inventory:
            return "Thou possesseth no fish to sell!"

        total_earned = 0
        summary = "**You step into the market and sell thy bounty:**\n"
        for name, info in st.session_state.inventory.items():
            count = info["count"]
            reward = next(f for f in FishPool if f["name"] == name)["reward"]
            earned = reward * count
            total_earned += earned
            summary += f"- **{info['rarity']} {name}** × {count} → 💰 +{earned} Fincoins\n"

        st.session_state.money += total_earned
        st.session_state.inventory = {}

        return summary + f"\n💰 **Total Earned:** {total_earned} Fincoins!"
    
    elif command == "/rod":
        rod = st.session_state.rod_level
        bait = st.session_state.current_bait
        bait_effect = BaitEffects.get(bait, BaitEffects["Worm Bait"])

        # Calculate adjusted weights per rarity
        rarity_totals = {"Common": 0, "Uncommon": 0, "Rare": 0, "Epic": 0, "Legendary": 0, "Mythical": 0}
        xp = st.session_state.experience
        level, _, _ = get_level_and_progress(xp)

        for fish in FishPool:
            rarity = fish["rarity"]
            base = fish["weight"]
            bonus = rod * 0.015
            bait_bonus = bait_effect[rarity]
            if rarity == "Common":
                adj = base * max(1.0 - (level * 0.02 + rod * 0.03), 0.1) * bait_bonus
            else:
                scale = {
                    "Uncommon": 0.01,
                    "Rare": 0.02,
                    "Epic": 0.025,
                    "Legendary": 0.03,
                    "Mythical": 0.04
                }[rarity]
                adj = base * (1.0 + level * scale + bonus) * bait_bonus
            rarity_totals[rarity] += adj

        total = sum(rarity_totals.values())

        rarity_chances = ""
        for rarity in ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythical"]:
            chance = (rarity_totals[rarity] / total) * 100
            rarity_chances += f"- **{rarity}**: {chance:.2f}%\n"

        bait_data = ""
        for r, mult in bait_effect.items():
            bait_data += f"- {r}: ×{mult}\n"

        return (
            f"🎣 **Rod Level:** {rod}\n"
            f"🧠 **Player Level:** {level}\n"
            f"🪱 **Current Bait:** {bait}\n\n"
            f"**🎯 Rarity Chances When Fishing:**\n{rarity_chances}\n"
            f"**🔬 Bait Effects (× Weight Multiplier):**\n{bait_data}"
        )

    elif command == "/shop":
        rod_cost = 50 * (st.session_state.rod_level + 1)
        bait_cost = 10

        st.markdown("### 🛒 The Bait & Tackle Shop")

        if st.button(f"Upgrade Rod (Lv.{st.session_state.rod_level}) → Lv.{st.session_state.rod_level + 1} for {rod_cost} Fincoins"):
            if st.session_state.money >= rod_cost:
                st.session_state.money -= rod_cost
                st.session_state.rod_level += 1
                st.success(f"🔧 Rod upgraded to Level {st.session_state.rod_level}!")
            else:
                st.error("Not enough Fincoins!")

        if st.button(f"Buy 5 Bait for {bait_cost} Fincoins"):
            if st.session_state.money >= bait_cost:
                st.session_state.money -= bait_cost
                st.session_state.bait += 5
                st.success("🪱 Purchased 5 bait!")
            else:
                st.error("Not enough Fincoins!")

        st.markdown("#### 🎯 Choose Your Bait")
        for bait in BaitEffects:
            if st.button(f"Switch to {bait}"):
                st.session_state.current_bait = bait
                st.success(f"🎣 You now use **{bait}**!")

        return (
            f"🎣 **Rod Level:** {st.session_state.rod_level}\n"
            f"🪱 **Bait:** {st.session_state.bait} | **Type:** {st.session_state.current_bait}\n"
            f"💰 **Upgrade Cost:** {rod_cost} Fincoins\n"
            f"💰 **Bait Cost:** {bait_cost} Fincoins (for 5)"
        )

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
if "rod_level" not in st.session_state:
    st.session_state.rod_level = 0
if "bait" not in st.session_state:
    st.session_state.bait = 10
if "current_bait" not in st.session_state:
    st.session_state.current_bait = "Worm Bait"

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
