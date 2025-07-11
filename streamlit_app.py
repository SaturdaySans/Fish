import streamlit as st
import random
import time
from fish_data import FishPool, BaitEffects

st.title("🐟 Fishing Simulator")

BaitPrices = {
    "Worm Bait": 10,
    "Rock Bait": 5,
    "Salt Bait": 25,
    "Golden Bait": 50
}

TreasureBoosts = {
    "Ancient Pearl": "sell_bonus",
    "Lost King’s Crown": "rod_bonus",
    "Sunken Map Fragment": "xp_bonus",
    "Enchanted Compass": "common_reduction"
}

def get_level_and_progress(experience):
    level = int(experience ** 0.5)
    next_level_xp = (level + 1) ** 2
    current_level_xp = level ** 2
    progress = experience - current_level_xp
    needed = next_level_xp - current_level_xp
    return level, progress, needed

def go_fishing():
    xp = st.session_state.experience
    level, _, _ = get_level_and_progress(xp)
    rod_level = st.session_state.rod_level + st.session_state.treasure_boosts.get("rod_bonus", 0)
    bait = st.session_state.current_bait
    bait_effect = BaitEffects.get(bait, BaitEffects["Worm Bait"])

    adjusted_weights = []
    for f in FishPool:
        rarity = f["rarity"]
        base = f["weight"]
        bonus = rod_level * 0.015
        rarity_bonus = bait_effect.get(rarity, 1.0)

        if rarity == "Common":
            reduction = st.session_state.treasure_boosts.get("common_reduction", 0)
            common_factor = max(1.0 - (level * 0.02 + rod_level * 0.03 + reduction), 0.05)
            adjusted = base * common_factor * rarity_bonus
        elif rarity == "Treasure":
            adjusted = base * rarity_bonus
        else:
            scale = {"Uncommon": 0.01, "Rare": 0.02, "Epic": 0.025, "Legendary": 0.03, "Mythical": 0.04}[rarity]
            adjusted = base * (1.0 + level * scale + bonus) * rarity_bonus
        adjusted_weights.append(adjusted)

    names = [f["name"] for f in FishPool]
    chosen_name = random.choices(names, weights=adjusted_weights, k=1)[0]
    return next(f for f in FishPool if f["name"] == chosen_name)

def handle_command(command):
    command = command.strip().lower()

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Cast thy rod\n"
            "- `/autofish` — Auto fish up to 10 🤖\n"
            "- `/inventory` — Basket 🧺\n"
            "- `/sell` — Sell fish 💰\n"
            "- `/money` — Fincoins 💰\n"
            "- `/experience` — XP & Level ✨\n"
            "- `/rod` — Rod stats 🎯\n"
            "- `/shop` — Upgrade rod, buy bait 🛒\n"
            "- `/dictionary` — Fish caught 📖\n"
            "- `/treasure` — Treasure boosts 💎\n"
            "- `/achievements` — Milestones 🏆"
        )

    elif command == "/fish":
        bait = st.session_state.current_bait
        if st.session_state.bait_inventory.get(bait, 0) <= 0:
            return "No bait! Use `/shop` to buy more."
        catch = go_fishing()
        xp = 1
        if st.session_state.treasure_boosts.get("xp_bonus"): xp = int(xp * 1.5)
        st.session_state.experience += xp
        st.session_state.bait_inventory[bait] -= 1
        st.session_state.dictionary.add(catch["name"])
        if catch["rarity"] == "Treasure":
            effect = TreasureBoosts[catch["name"]]
            if effect == "sell_bonus": st.session_state.treasure_boosts["sell_bonus"] = 0.2
            elif effect == "rod_bonus": st.session_state.treasure_boosts["rod_bonus"] = 5
            elif effect == "xp_bonus": st.session_state.treasure_boosts["xp_bonus"] = True
            elif effect == "common_reduction": st.session_state.treasure_boosts["common_reduction"] = 0.3
            return f"🌟 Found treasure: **{catch['name']}**! Boost unlocked!"
        st.session_state.inventory[catch["name"]] = st.session_state.inventory.get(catch["name"], {"rarity": catch["rarity"], "count":0})
        st.session_state.inventory[catch["name"]]["count"] += 1
        return f"You caught a **{catch['rarity']} {catch['name']}**!"

    elif command == "/autofish":
        bait = st.session_state.current_bait
        if st.session_state.bait_inventory.get(bait, 0) <= 0:
            return "No bait! Buy more with `/shop`."
        result = []
        for _ in range(10):
            if st.session_state.bait_inventory[bait] <= 0: break
            catch = go_fishing()
            xp = 1
            if st.session_state.treasure_boosts.get("xp_bonus"): xp = int(xp * 1.5)
            st.session_state.experience += xp
            st.session_state.bait_inventory[bait] -= 1
            st.session_state.dictionary.add(catch["name"])
            if catch["rarity"] == "Treasure":
                effect = TreasureBoosts[catch["name"]]
                if effect == "sell_bonus": st.session_state.treasure_boosts["sell_bonus"] = 0.2
                elif effect == "rod_bonus": st.session_state.treasure_boosts["rod_bonus"] = 5
                elif effect == "xp_bonus": st.session_state.treasure_boosts["xp_bonus"] = True
                elif effect == "common_reduction": st.session_state.treasure_boosts["common_reduction"] = 0.3
                result.append(f"- Treasure: {catch['name']}")
            else:
                st.session_state.inventory[catch["name"]] = st.session_state.inventory.get(catch["name"], {"rarity": catch["rarity"], "count":0})
                st.session_state.inventory[catch["name"]]["count"] += 1
                result.append(f"- {catch['rarity']} {catch['name']}")
        return "Auto-fished:\n" + "\n".join(result)

    elif command == "/treasure":
        boosts = st.session_state.treasure_boosts
        if not boosts: return "🔒 No treasures yet!"
        return "\n".join([f"- {k}: {v}" for k,v in boosts.items()])

    elif command == "/achievements":
        unique = len(st.session_state.dictionary)
        treasures = len(st.session_state.treasure_boosts)
        lvl,_,_ = get_level_and_progress(st.session_state.experience)
        return f"🏆 Achievements:\n- Unique Fish: {unique}\n- Treasures: {treasures}\n- Level: {lvl}"

    elif command == "/inventory":
        if not st.session_state.inventory: return "Empty!"
        return "\n".join([f"{k} x{v['count']}" for k,v in st.session_state.inventory.items()])

    elif command == "/money":
        return f"💰 Fincoins: {st.session_state.money}"

    elif command == "/experience":
        lvl,p,n = get_level_and_progress(st.session_state.experience)
        return f"Level {lvl} — {p}/{n} XP"

    # ADD your `/sell`, `/rod`, `/shop`, `/dictionary` SAME as before!
    # KEEP your rod/shop/buttons exactly as you had them.

    else:
        return "Unknown command."

# ✅ States
if "messages" not in st.session_state: st.session_state.messages = []
if "money" not in st.session_state: st.session_state.money = 0
if "experience" not in st.session_state: st.session_state.experience = 0
if "inventory" not in st.session_state: st.session_state.inventory = {}
if "rod_level" not in st.session_state: st.session_state.rod_level = 0
if "bait_inventory" not in st.session_state: st.session_state.bait_inventory = {"Worm Bait": 10}
if "current_bait" not in st.session_state: st.session_state.current_bait = "Worm Bait"
if "dictionary" not in st.session_state: st.session_state.dictionary = set()
if "treasure_boosts" not in st.session_state: st.session_state.treasure_boosts = {}

# ✅ Chat loop stays alive!
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Type command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    response = handle_command(prompt)
    with st.chat_message("assistant"): st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
