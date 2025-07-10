import streamlit as st
import random
import time
from fish_data import FishPool, BaitEffects

st.title("🐟 Fishing Simulator")

# 💰 Bait Prices
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
            "- `/money` — View thy wealth 💰\n"
            "- `/experience` — Check thy fishing level ✨\n"
            "- `/shop` — Upgrade rod / Buy bait 🎣\n"
            "- `/rod` — Check stats / Switch bait 🎯\n"
            "- `/dictionary` — View fish you’ve discovered 📖\n"
            "- `/help` — This guide of holy waters"
        )

    elif command == "/fish":
        bait = st.session_state.current_bait
        bait_count = st.session_state.bait_inventory.get(bait, 0)
        if bait_count <= 0:
            return f"🪱 You have no **{bait}**! Visit the `/shop` to buy more."

        catch = go_fishing()
        st.session_state.experience += 1
        st.session_state.bait_inventory[bait] -= 1

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

        name = catch["name"]
        if name in st.session_state.inventory:
            st.session_state.inventory[name]["count"] += 1
        else:
            st.session_state.inventory[name] = {"rarity": catch["rarity"], "count": 1}
        st.session_state.dictionary.add(name)

        return (
            f"You cast your rod... and lo! You caught a **{catch['rarity']} {name}**! 🐟\n"
            f"✨ +1 XP | 🪱 -1 {bait} (Remaining: {st.session_state.bait_inventory[bait]})\n"
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

        bait_data = "\n".join(f"- {r}: ×{mult}" for r, mult in bait_effect.items())

        baits_owned = "\n".join(f"- {bait}: {qty}" for bait, qty in st.session_state.bait_inventory.items())

        return (
            f"🎣 **Rod Level:** {rod}\n"
            f"🧠 **Player Level:** {level}\n"
            f"🪱 **Current Bait:** {bait}\n\n"
            f"**🎯 Rarity Chances:**\n{rarity_chances}\n"
            f"**🔬 Bait Effects:**\n{bait_data}\n"
            f"**📦 Baits Owned:**\n{baits_owned}\n\n"
            f"⬇️ Switch bait using buttons below."
        )

    elif command == "/shop":
        baits = "\n".join(
            f"- {bait}: {qty}" for bait, qty in st.session_state.bait_inventory.items()
        )
        return (
            f"🎣 **Rod Level:** {st.session_state.rod_level}\n"
            f"🧠 **Player Level:** {get_level_and_progress(st.session_state.experience)[0]}\n"
            f"**Baits Owned:**\n{baits}\n"
            f"**Current Bait:** {st.session_state.current_bait}"
        )

    elif command == "/dictionary":
        seen = st.session_state.dictionary
        data = []
        for fish in FishPool:
            name = fish["name"]
            rarity = fish["rarity"]
            status = name if name in seen else "[Locked]"
            data.append({"Rarity": rarity, "Name": status})
        st.dataframe(data)
        return "**Above is thy Fish Dictionary.**"

    else:
        return "Unknown command. Use `/help` to consult the waves of wisdom."

# 🌊 State Init
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
if "bait_inventory" not in st.session_state:
    st.session_state.bait_inventory = {"Worm Bait": 10}
if "current_bait" not in st.session_state:
    st.session_state.current_bait = "Worm Bait"
if "dictionary" not in st.session_state:
    st.session_state.dictionary = set()
if "last_command" not in st.session_state:
    st.session_state.last_command = ""

# 📜 Show chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💬 Process input
if prompt := st.chat_input("Type /fish, /rod, /shop, etc."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = handle_command(prompt)
    st.session_state.last_command = prompt.strip().lower()

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 🪱 Bait switcher for /rod
if st.session_state.last_command == "/rod":
    st.markdown("#### 🎯 Switch Bait")
    for bait_option, qty in st.session_state.bait_inventory.items():
        if qty > 0 and st.button(f"Use {bait_option} ({qty})"):
            st.session_state.current_bait = bait_option
            st.success(f"🎣 Now using **{bait_option}**!")
            st.rerun()

# 🛒 Shop for /shop
if st.session_state.last_command == "/shop":
    rod_cost = 50 * (st.session_state.rod_level + 1)

    if st.button(f"Upgrade Rod to Lv.{st.session_state.rod_level + 1} ({rod_cost} Fincoins)"):
        if st.session_state.money >= rod_cost:
            st.session_state.money -= rod_cost
            st.session_state.rod_level += 1
            st.success("🔧 Rod upgraded!")
        else:
            st.error("Too poor!")

    st.markdown("#### 🪱 Buy Bait")
    for bait, price in BaitPrices.items():
        if st.button(f"Buy 5 × {bait} ({price} Fincoins)"):
            if st.session_state.money >= price:
                st.session_state.money -= price
                st.session_state.bait_inventory[bait] = st.session_state.bait_inventory.get(bait, 0) + 5
                st.success(f"🪱 Bought 5 × {bait}!")
            else:
                st.error("Too poor!")
