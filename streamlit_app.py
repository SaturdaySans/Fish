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
            scale = {
                "Uncommon": 0.01, "Rare": 0.02, "Epic": 0.025,
                "Legendary": 0.03, "Mythical": 0.04
            }[rarity]
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
            "- `/autofish` — Auto fish up to 10 times 🤖\n"
            "- `/inventory` — View your fish 🧺\n"
            "- `/sell` — Sell fish 💰\n"
            "- `/money` — View Fincoins 💰\n"
            "- `/experience` — Check XP ✨\n"
            "- `/shop` — Upgrade rod / Buy bait 🎣\n"
            "- `/rod` — Stats & Switch bait 🎯\n"
            "- `/dictionary` — Fish discovered 📖\n"
            "- `/treasure` — Your treasure boosts 💎\n"
            "- `/achievements` — Your milestones 🏆\n"
            "- `/help` — This guide"
        )

    elif command == "/fish":
        bait = st.session_state.current_bait
        bait_count = st.session_state.bait_inventory.get(bait, 0)
        if bait_count <= 0:
            return f"🪱 You have no **{bait}**! Use `/shop` to buy more."

        catch = go_fishing()

        xp_gain = 1
        if "xp_bonus" in st.session_state.treasure_boosts:
            xp_gain = int(xp_gain * 1.5)

        st.session_state.experience += xp_gain
        st.session_state.bait_inventory[bait] -= 1

        rarity = catch["rarity"]
        delay_map = {
            "Common": (0.5, 1.0),
            "Uncommon": (1.0, 1.5),
            "Rare": (1.5, 2.0),
            "Epic": (2.0, 2.5),
            "Legendary": (2.5, 3.0),
            "Mythical": (3.0, 3.5),
            "Treasure": (4.0, 5.0)
        }
        time.sleep(random.uniform(*delay_map[rarity]))

        name = catch["name"]
        st.session_state.dictionary.add(name)

        if rarity == "Treasure":
            if TreasureBoosts[name] not in st.session_state.treasure_boosts:
                if TreasureBoosts[name] == "sell_bonus":
                    st.session_state.treasure_boosts["sell_bonus"] = 0.2
                elif TreasureBoosts[name] == "rod_bonus":
                    st.session_state.treasure_boosts["rod_bonus"] = 5
                elif TreasureBoosts[name] == "xp_bonus":
                    st.session_state.treasure_boosts["xp_bonus"] = True
                elif TreasureBoosts[name] == "common_reduction":
                    st.session_state.treasure_boosts["common_reduction"] = 0.3

            return (
                f"🌟 You found a **Treasure: {name}**! It grants you a permanent boost! 🎁\n"
                f"✨ +{xp_gain} XP | 🪱 -1 {bait} ({st.session_state.bait_inventory[bait]} left)"
            )
        else:
            if name in st.session_state.inventory:
                st.session_state.inventory[name]["count"] += 1
            else:
                st.session_state.inventory[name] = {"rarity": catch["rarity"], "count": 1}

            return (
                f"You caught a **{catch['rarity']} {name}**! 🐟\n"
                f"✨ +{xp_gain} XP | 🪱 -1 {bait} ({st.session_state.bait_inventory[bait]} left)"
            )

    elif command == "/autofish":
        bait = st.session_state.current_bait
        bait_count = st.session_state.bait_inventory.get(bait, 0)
        if bait_count <= 0:
            return f"🪱 You have no **{bait}**! Use `/shop` to buy more."

        results = []
        for _ in range(10):
            if st.session_state.bait_inventory[bait] <= 0:
                break

            catch = go_fishing()

            xp_gain = 1
            if "xp_bonus" in st.session_state.treasure_boosts:
                xp_gain = int(xp_gain * 1.5)

            st.session_state.experience += xp_gain
            st.session_state.bait_inventory[bait] -= 1

            name = catch["name"]
            st.session_state.dictionary.add(name)

            if catch["rarity"] == "Treasure":
                if TreasureBoosts[name] not in st.session_state.treasure_boosts:
                    if TreasureBoosts[name] == "sell_bonus":
                        st.session_state.treasure_boosts["sell_bonus"] = 0.2
                    elif TreasureBoosts[name] == "rod_bonus":
                        st.session_state.treasure_boosts["rod_bonus"] = 5
                    elif TreasureBoosts[name] == "xp_bonus":
                        st.session_state.treasure_boosts["xp_bonus"] = True
                    elif TreasureBoosts[name] == "common_reduction":
                        st.session_state.treasure_boosts["common_reduction"] = 0.3
                results.append(f"- 🌟 Treasure: **{name}**")
            else:
                if name in st.session_state.inventory:
                    st.session_state.inventory[name]["count"] += 1
                else:
                    st.session_state.inventory[name] = {"rarity": catch["rarity"], "count": 1}
                results.append(f"- **{catch['rarity']} {name}**")

        return (
            f"🤖 You auto-fished:\n" + "\n".join(results) +
            f"\n✨ +{len(results)} XP | 🪱 -{len(results)} {bait} ({st.session_state.bait_inventory[bait]} left)"
        )

    elif command == "/treasure":
        boosts = st.session_state.treasure_boosts
        if not boosts:
            return "🔒 No treasures yet! Keep fishing!"
        response = "**🎁 Your Active Treasure Boosts:**\n"
        for name, effect in TreasureBoosts.items():
            if effect in boosts:
                if effect == "sell_bonus":
                    response += "- 💰 **Ancient Pearl:** +20% sell bonus\n"
                elif effect == "rod_bonus":
                    response += "- 🎣 **Lost King’s Crown:** +5 rod levels\n"
                elif effect == "xp_bonus":
                    response += "- ✨ **Sunken Map Fragment:** +50% XP gain\n"
                elif effect == "common_reduction":
                    response += "- 🐟 **Enchanted Compass:** Common fish are less common\n"
        return response

    elif command == "/achievements":
        unique_fish = len(st.session_state.dictionary)
        treasures = len(st.session_state.treasure_boosts)
        level, _, _ = get_level_and_progress(st.session_state.experience)
        return (
            "**🏆 Achievements:**\n"
            f"- 📚 **Unique Fish Caught:** {unique_fish}\n"
            f"- 💎 **Treasures Found:** {treasures}\n"
            f"- 🎣 **Current Level:** {level}\n"
        )

    # KEEP ALL REMAINING COMMANDS SAME
    # (Reuse your sell, money, experience, inventory, rod, shop, dictionary from before)

    elif command == "/sell":
        if not st.session_state.inventory:
            return "No fish to sell!"
        level, _, _ = get_level_and_progress(st.session_state.experience)
        sell_bonus = 1 + (level * 0.02) + st.session_state.treasure_boosts.get("sell_bonus", 0)
        total = 0
        summary = "**You sold your fish:**\n"
        for name, info in st.session_state.inventory.items():
            base = next(f for f in FishPool if f["name"] == name)["reward"]
            adjusted = int(base * sell_bonus)
            earned = adjusted * info["count"]
            total += earned
            summary += f"- **{info['rarity']} {name}** × {info['count']} → +{earned} Fincoins\n"
        st.session_state.money += total
        st.session_state.inventory = {}
        return summary + f"\n💰 **Total:** {total} Fincoins! (+{int((sell_bonus-1)*100)}% bonus)"

    # Add your other unchanged parts here (money, experience, rod, shop, dictionary)

# ⚙️ State Initialization
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
if "treasure_boosts" not in st.session_state:
    st.session_state.treasure_boosts = {}
if "last_command" not in st.session_state:
    st.session_state.last_command = ""

# 🗨️ Chat loop remains unchanged
# 🗨️ Switch bait/shop remains unchanged
