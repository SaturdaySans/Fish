import streamlit as st
import random
import time
from fish_data import FishPool, BaitEffects, FishingLocations

st.title("🐟 Fishing Simulator")

BaitPrices = {
    "Worm Bait": 2,
    "Rock Bait": 1,
    "Salt Bait": 5,
    "Golden Bait": 10
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
    location_mod = FishingLocations.get(st.session_state.current_location, {}).get("modifiers", {})

    adjusted_weights = []
    for f in FishPool:
        rarity = f["rarity"]
        base = f["weight"]
        bonus = rod_level * 0.015
        rarity_bonus = bait_effect.get(rarity, 1.0)
        location_bonus = location_mod.get(rarity, 1.0)

        if rarity == "Common":
            reduction = st.session_state.treasure_boosts.get("common_reduction", 0)
            common_factor = max(1.0 - (level * 0.02 + rod_level * 0.03 + reduction), 0.05)
            adjusted = base * common_factor * rarity_bonus * location_bonus
        elif rarity == "Treasure":
            scale = 0.05
            adjusted = base * (1.0 + level * scale + bonus) * rarity_bonus * location_bonus
        else:
            scale = {
                "Uncommon": 0.01, "Rare": 0.02, "Epic": 0.025,
                "Legendary": 0.03, "Mythical": 0.04
            }[rarity]
            adjusted = base * (1.0 + level * scale + bonus) * rarity_bonus * location_bonus

        adjusted_weights.append(adjusted)

    names = [f["name"] for f in FishPool]
    chosen_name = random.choices(names, weights=adjusted_weights, k=1)[0]
    return next(f for f in FishPool if f["name"] == chosen_name)

def handle_command(command):
    command = command.strip().lower()

    if command == "/travel":
        st.markdown("## 🧭 Travel to Another Location")
        xp = st.session_state.experience
        unlocked_locations = {
            name: data for name, data in FishingLocations.items()
            if get_level_and_progress(xp)[0] >= data.get("min_exp", 0)  # level-based unlock
        }

        if not unlocked_locations:
            st.write("❌ Thou hast not unlocked any new lands to explore yet!")
            return ""

        # Initialize session state for travel selection if not present
        if "travel_select" not in st.session_state:
            st.session_state.travel_select = list(unlocked_locations.keys())[0]

        # Show dropdown with saved selection
        selected = st.selectbox("🌍 Choose thy destination", list(unlocked_locations.keys()), index=list(unlocked_locations.keys()).index(st.session_state.travel_select), key="travel_select")

        # Travel button
        if st.button("Travel There"):
            st.session_state.current_location = selected
            st.success(f"📍 You travelled to **{selected}**!\n🌊 {unlocked_locations[selected]['description']}")

        # Return empty string or None so no "replace all UI" string is shown
        return ""

    elif command.startswith("/travel "):
        loc_input = command.split(" ", 1)[1].strip().lower()
        matched_loc = None
        for key in FishingLocations:
            if key.lower() == loc_input:
                matched_loc = key
                break

        if matched_loc:
            required = FishingLocations[matched_loc]["min_exp"]
            if st.session_state.experience >= required:
                st.session_state.current_location = matched_loc
                return f"📍 You travelled to **{matched_loc}**!\n🌊 {FishingLocations[matched_loc]['description']}"
            else:
                return f"🔒 That location is locked! Requires **{required} EXP** to unlock."
        else:
            return "❌ Unknown location. Try `/travel` to see options."
    
    elif command == "/location":
        loc = st.session_state.current_location
        data = FishingLocations.get(loc)
        if data:
            desc = data.get("description", "No description")
            return f"📍 **Current Location:** {loc}\n🌊 {desc}"
        else:
            return "❓ Unknown location!"

    if command == "/help":
        return (
            "**Available Commands:**\n"
            "- `/fish` — Cast thy rod\n"
            "- `/autofish` — Auto fish 5 times (lower rare odds) 🤖\n"
            "- `/inventory` — View your fish 🧺\n"
            "- `/sell` — Sell fish 💰\n"
            "- `/money` — View Fincoins 💰\n"
            "- `/experience` — Check XP ✨\n"
            "- `/shop` — Upgrade rod / Buy bait 🎣\n"
            "- `/rod` — Stats & Switch bait 🎯\n"
            "- `/dictionary` — Fish discovered 📖\n"
            "- `/treasure` — See your treasure boosts 🧭\n"
            "- `/travel` — View & change fishing location 🧳\n"
            "- `/location` — See where you are & its effects 🌍"
        )

    if command == "/fish":
        bait = st.session_state.current_bait
        bait_count = st.session_state.bait_inventory.get(bait, 0)
        if bait_count <= 0:
            return f"🪱 You have no **{bait}**! Use `/shop` to buy more."

        catch = go_fishing()

        # ❗ FIXED XP BONUS LOGIC
        xp_gain = 1
        if "xp_bonus" in st.session_state.treasure_boosts:
            xp_gain += 0.5  # +50%

        st.session_state.experience += xp_gain
        st.session_state.bait_inventory[bait] -= 1

        # ... [delay & result logic unchanged] ...
        name = catch["name"]
        rarity = catch["rarity"]
        st.session_state.dictionary.add(name)

        if rarity == "Treasure":
            if TreasureBoosts[name] not in st.session_state.treasure_boosts:
                effect = TreasureBoosts[name]
                if effect == "sell_bonus":
                    st.session_state.treasure_boosts["sell_bonus"] = 0.2
                elif effect == "rod_bonus":
                    st.session_state.treasure_boosts["rod_bonus"] = 5
                elif effect == "xp_bonus":
                    st.session_state.treasure_boosts["xp_bonus"] = True
                elif effect == "common_reduction":
                    st.session_state.treasure_boosts["common_reduction"] = 0.3

            return (
                f"🌟 You found a **Treasure: {name}**! It grants you a permanent boost! 🎁\n"
                f"✨ +{xp_gain} XP | 🪱 -1 {bait} ({st.session_state.bait_inventory[bait]} left)"
            )
        else:
            if name in st.session_state.inventory:
                st.session_state.inventory[name]["count"] += 1
            else:
                st.session_state.inventory[name] = {"rarity": rarity, "count": 1}

            return (
                f"You caught a **{rarity} {name}**! 🐟\n"
                f"✨ +{xp_gain} XP | 🪱 -1 {bait} ({st.session_state.bait_inventory[bait]} left)"
            )

    elif command == "/autofish":
        bait = st.session_state.current_bait
        bait_count = st.session_state.bait_inventory.get(bait, 0)
        if bait_count <= 0:
            return f"🪱 You have no **{bait}**! Use `/shop` to buy more."

        results = []
        xp_total = 0  # ✅ Sum raw XP gains
        for _ in range(25):
            if st.session_state.bait_inventory[bait] <= 0:
                break

            catch = go_fishing()

            xp_gain = 1
            if "xp_bonus" in st.session_state.treasure_boosts:
                xp_gain += 0.5  # ✅ True +50%

            xp_total += xp_gain
            st.session_state.bait_inventory[bait] -= 1

            name = catch["name"]
            rarity = catch["rarity"]
            st.session_state.dictionary.add(name)

            if rarity == "Treasure":
                if TreasureBoosts[name] not in st.session_state.treasure_boosts:
                    effect = TreasureBoosts[name]
                    if effect == "sell_bonus":
                        st.session_state.treasure_boosts["sell_bonus"] = 0.2
                    elif effect == "rod_bonus":
                        st.session_state.treasure_boosts["rod_bonus"] = 5
                    elif effect == "xp_bonus":
                        st.session_state.treasure_boosts["xp_bonus"] = True
                    elif effect == "common_reduction":
                        st.session_state.treasure_boosts["common_reduction"] = 0.3
                results.append(f"- 🌟 Treasure: **{name}**")
            else:
                if name in st.session_state.inventory:
                    st.session_state.inventory[name]["count"] += 1
                else:
                    st.session_state.inventory[name] = {"rarity": rarity, "count": 1}
                results.append(f"- **{rarity} {name}**")

        st.session_state.experience += xp_total  # ✅ Total fractional XP applied here
        return (
            f"🤖 You auto-fished:\n" + "\n".join(results) +
            f"\n✨ +{xp_total} XP | 🪱 -{len(results)} {bait} ({st.session_state.bait_inventory[bait]} left)"
        )

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

    elif command == "/money":
        return f"You have **{st.session_state.money} Fincoins**. 💰"

    elif command == "/experience":
        xp = int(st.session_state.experience)
        level, progress, needed = get_level_and_progress(xp)
        sell_bonus = int(level * 2) + int(st.session_state.treasure_boosts.get("sell_bonus", 0) * 100)

        st.markdown(f"**Level {level}** — {progress}/{needed} XP to next level ✨")
        st.progress(progress / needed)
        return (
            f"**Your Fishing Experience:**\n"
            f"- 🎣 **Level:** {level} (XP: {xp})\n"
            f"- 📈 **Sell Bonus:** +{sell_bonus}% profit\n"
            f"- ⚙️ **Rod Bonus:** +{st.session_state.treasure_boosts.get('rod_bonus', 0)} levels\n"
            f"- 📖 **Treasures Discovered:** {len(st.session_state.treasure_boosts)} boosts active"
        )

    elif command == "/inventory":
        if not st.session_state.inventory:
            return "Your basket is empty!"
        response = "**Your Inventory:**\n"
        for name, info in st.session_state.inventory.items():
            response += f"- **{info['rarity']} {name}** × {info['count']}\n"
        return response

    elif command == "/treasure":
        boosts = st.session_state.treasure_boosts
        if not boosts:
            return "🔍 Thou possesseth no treasures yet... Seek the abyss!"

        treasure_names = {
            "sell_bonus": "Ancient Pearl",
            "rod_bonus": "Lost King’s Crown",
            "xp_bonus": "Sunken Map Fragment",
            "common_reduction": "Enchanted Compass"
        }

        descriptions = {
            "sell_bonus": "+20% more Fincoins from selling fish",
            "rod_bonus": "+5 bonus rod levels when fishing",
            "xp_bonus": "+50% XP gain from each catch",
            "common_reduction": "-30% chance of catching Common fish"
        }

        response = "**🧭 Active Treasures:**\n"
        for key in boosts:
            if key in treasure_names:
                name = treasure_names[key]
                desc = descriptions[key]
                response += f"- 🌟 **{name}** → {desc}\n"
        return response


    elif command == "/rod":
        rod = st.session_state.rod_level + st.session_state.treasure_boosts.get("rod_bonus", 0)
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
                reduction = st.session_state.treasure_boosts.get("common_reduction", 0)
                adj = base * max(1.0 - (level * 0.02 + rod * 0.03 + reduction), 0.05) * bait_bonus
            else:
                if rarity == "Treasure":
                    adj = base * bait_bonus
                else:
                    scale = {"Uncommon": 0.01, "Rare": 0.02, "Epic": 0.025,
                             "Legendary": 0.03, "Mythical": 0.04}[rarity]
                    adj = base * (1.0 + level * scale + bonus) * bait_bonus
            rarity_totals[rarity] += adj

        total = sum(rarity_totals.values())
        rarity_chances = "\n".join(
            f"- **{r}**: {(rarity_totals[r] / total) * 100:.2f}%" for r in rarity_totals
        )
        bait_data = "\n".join(f"- {r}: ×{mult}" for r, mult in bait_effect.items())
        baits_owned = "\n".join(f"- {b}: {q}" for b, q in st.session_state.bait_inventory.items())

        return (
            f"🎣 **Rod Level:** {rod}\n"
            f"🧠 **Player Level:** {level}\n"
            f"🪱 **Current Bait:** {bait}\n\n"
            f"**🎯 Rarity Chances:**\n{rarity_chances}\n"
            f"**🔬 Bait Effects:**\n{bait_data}\n"
            f"**📦 Baits Owned:**\n{baits_owned}\n"
        )

    elif command == "/shop":
        baits = "\n".join(f"- {b}: {q}" for b, q in st.session_state.bait_inventory.items())
        return (
            f"🎣 **Rod Level:** {st.session_state.rod_level}\n"
            f"**Baits Owned:**\n{baits}\n"
            f"**Current Bait:** {st.session_state.current_bait}"
        )

    elif command == "/dictionary":
        seen = st.session_state.dictionary
        data = []
        for fish in FishPool:
            name = fish["name"]
            rarity = fish["rarity"]
            reward = fish["reward"]
            status = name if name in seen else "[Locked]"
            data.append({"Rarity": rarity, "Name": status, "Base Reward": reward})
        st.dataframe(data)
        return "**Above is your Fish Dictionary.**"

    else:
        return "Unknown command."

# States
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
if "current_location" not in st.session_state:
    st.session_state.current_location = "Crystal Shoals"  # 🧭 Must match FishingLocations key
if "travel_mode" not in st.session_state:
    st.session_state.travel_mode = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type /fish, /rod, /shop, /travel, etc."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.last_command = prompt.strip().lower()
    st.session_state.travel_mode = (st.session_state.last_command == "/travel")

    response = handle_command(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.last_command == "/rod":
    st.markdown("#### 🎯 Switch Bait")
    for bait, qty in st.session_state.bait_inventory.items():
        if qty > 0 and st.button(f"Use {bait} ({qty})"):
            st.session_state.current_bait = bait
            st.success(f"🎣 Now using **{bait}**!")
            st.rerun()

if st.session_state.last_command == "/shop":
    rod_cost = 50 * (st.session_state.rod_level + 1)
    if st.button(f"Upgrade Rod Lv.{st.session_state.rod_level} → Lv.{st.session_state.rod_level+1} ({rod_cost} Fincoins)"):
        if st.session_state.money >= rod_cost:
            st.session_state.money -= rod_cost
            st.session_state.rod_level += 1
            st.success("🔧 Rod upgraded!")
        else:
            st.error("Too poor!")

    st.markdown("#### 🪱 Buy Bait")
    for bait, price in BaitPrices.items():
        qty = st.slider(
            f"Select quantity for {bait} ({price} Fincoins each)",
            min_value=1, max_value=100, key=f"slider_{bait}"
        )
        if st.button(f"Buy {qty} × {bait} ({price * qty} Fincoins)", key=f"buy_button_{bait}"):
            total_price = price * qty
            if st.session_state.money >= total_price:
                st.session_state.money -= total_price
                st.session_state.bait_inventory[bait] = st.session_state.bait_inventory.get(bait, 0) + qty
                st.success(f"Bought {qty} × {bait}!")
            else:
                st.error("Too poor!")

    st.markdown("#### 🪱 Quick Buy: 5x Each Bait")
    for bait, price in BaitPrices.items():
        total_price = price * 5
        if st.button(f"Buy 5 × {bait} ({total_price} Fincoins)", key=f"quickbuy_{bait}"):
            if st.session_state.money >= total_price:
                st.session_state.money -= total_price
                st.session_state.bait_inventory[bait] = st.session_state.bait_inventory.get(bait, 0) + 5
                st.success(f"Bought 5 × {bait}!")
            else:
                st.error("Too poor!")
