import streamlit as st
import random
import time
from fish_data import FishPool, BaitEffects

st.title("🐟 Fishing Simulator")

# 💰 Custom Bait Prices
BaitPrices = {
    "Worm Bait": 10,
    "Rock Bait": 15,
    "Salt Bait": 25,
    "Golden Bait": 50
}

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
            - "/money` — View thy wealth 💰\n"
            "- `/experience` — Check thy fishing level ✨\n"
            "- `/shop` — Upgrade rod / Buy bait / Change bait 🎣\n"
            "- `/rod` — Check fishing stats / Switch bait 🎯\n"
            "- `/dictionary` — View fish you’ve discovered 📖\n"
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
        st.session_state.dictionary.add(name)

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
        rarity_totals = {r: 0 for r in BaitEffects["Worm Bait"]}
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
                    "Uncommon": 0.01, "Rare": 0.02, "Epic": 0.025,
                    "Legendary": 0.03, "Mythical": 0.04
                }[rarity]
                adj = base * (1.0 + level * scale + bonus) * bait_bonus
            rarity_totals[rarity] += adj

        total = sum(rarity_totals.values())
        rarity_chances = "\n".join(
            f"- **{r}**: {(rarity_totals[r] / total) * 100:.2f}%" for r in rarity_totals
        )

        st.markdown("#### 🎯 Choose Your Bait")
        for bait_option in BaitEffects:
            if st.button(f"Switch to {bait_option}"):
                st.session_state.current_bait = bait_option
                st.success(f"🎣 You now use **{bait_option}**!")

        bait_data = "\n".join(f"- {r}: ×{mult}" for r, mult in bait_effect.items())

        return (
            f"🎣 **Rod Level:** {rod}\n"
            f"🧠 **Player Level:** {level}\n"
            f"🪱 **Current Bait:** {bait}\n\n"
            f"**🎯 Rarity Chances When Fishing:**\n{rarity_chances}\n"
            f"**🔬 Bait Effects (× Weight Multiplier):**\n{bait_data}"
        )

    elif command == "/shop":
        return (
            f"🎣 **Rod Level:** {st.session_state.rod_level}\n"
            f"🪱 **Bait:** {st.session_state.bait} | **Type:** {st.session_state.current_bait}\n"
        )

    elif command == "/dictionary":
        seen = st.session_state.dictionary
        response = "**📖 Fish Discovered:**\n"
        for fish in FishPool:
            name = fish["name"]
            rarity = fish["rarity"]
            if name in seen:
                response += f"- **{rarity} {name}**\n"
            else:
                response += f"- **{rarity} [Locked]**\n"
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
if "rod_level" not in st.session_state:
    st.session_state.rod_level = 0
if "bait" not in st.session_state:
    st.session_state.bait = 10
if "current_bait" not in st.session_state:
    st.session_state.current_bait = "Worm Bait"
if "dictionary" not in st.session_state:
    st.session_state.dictionary = set()
if "last_command" not in st.session_state:
    st.session_state.last_command = ""

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
    st.session_state.last_command = prompt.strip().lower()

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 🛒 Render shop UI if /shop was the last command
if st.session_state.last_command == "/shop":
    rod_cost = 50 * (st.session_state.rod_level + 1)

    if st.button(f"Upgrade Rod (Lv.{st.session_state.rod_level}) → Lv.{st.session_state.rod_level + 1} for {rod_cost} Fincoins"):
        if st.session_state.money >= rod_cost:
            st.session_state.money -= rod_cost
            st.session_state.rod_level += 1
            st.success(f"🔧 Rod upgraded to Level {st.session_state.rod_level}!")
        else:
            st.error("Not enough Fincoins!")

    st.markdown("#### 🪱 Buy Bait")
    for bait, price in BaitPrices.items():
        if st.button(f"Buy 5 × {bait} for {price} Fincoins"):
            if st.session_state.money >= price:
                st.session_state.money -= price
                st.session_state.bait += 5
                st.session_state.current_bait = bait
                st.success(f"🪱 Purchased 5 bait and switched to **{bait}**!")
            else:
                st.error("Not enough Fincoins!")
