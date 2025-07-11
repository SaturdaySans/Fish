# fish_data.py

# 🎏 Vast Pool of Fontaine's Finned Folk with Mythical Additions
FishPool = [
    # 🟢 Common
    {"name": "Salmon", "rarity": "Common", "weight": 50, "reward": 5},
    {"name": "Cod", "rarity": "Common", "weight": 50, "reward": 3},
    {"name": "Mackerel", "rarity": "Common", "weight": 40, "reward": 4},
    {"name": "Anchovy", "rarity": "Common", "weight": 45, "reward": 2},
    {"name": "Herring", "rarity": "Common", "weight": 40, "reward": 3},
    {"name": "Bubble Minnow", "rarity": "Common", "weight": 38, "reward": 2},
    {"name": "Drift Carp", "rarity": "Common", "weight": 35, "reward": 3},
    {"name": "Reed Perch", "rarity": "Common", "weight": 37, "reward": 4},

    # 🔵 Uncommon
    {"name": "Tuna", "rarity": "Uncommon", "weight": 20, "reward": 8},
    {"name": "Sardine Swarm", "rarity": "Uncommon", "weight": 20, "reward": 7},
    {"name": "Sea Bass", "rarity": "Uncommon", "weight": 18, "reward": 9},
    {"name": "Glass Snapper", "rarity": "Uncommon", "weight": 16, "reward": 10},
    {"name": "Dusky Grunt", "rarity": "Uncommon", "weight": 15, "reward": 11},
    {"name": "Velvet Tetra", "rarity": "Uncommon", "weight": 14, "reward": 10},

    # 🟣 Rare
    {"name": "Golden Carp", "rarity": "Rare", "weight": 10, "reward": 20},
    {"name": "Electric Eel", "rarity": "Rare", "weight": 10, "reward": 22},
    {"name": "Moon Jellyfish", "rarity": "Rare", "weight": 8, "reward": 18},
    {"name": "Stormfin Tuna", "rarity": "Rare", "weight": 7, "reward": 25},
    {"name": "Twilight Piranha", "rarity": "Rare", "weight": 6, "reward": 24},
    {"name": "Blazing Guppy", "rarity": "Rare", "weight": 6, "reward": 26},

    # 🟠 Epic
    {"name": "Swordfish", "rarity": "Epic", "weight": 5, "reward": 40},
    {"name": "Ornamental Koi", "rarity": "Epic", "weight": 4, "reward": 35},
    {"name": "Crystal Lionfish", "rarity": "Epic", "weight": 3, "reward": 50},
    {"name": "Echo Stingray", "rarity": "Epic", "weight": 2, "reward": 55},
    {"name": "Frost Pike", "rarity": "Epic", "weight": 2, "reward": 48},
    {"name": "Aetherfin Marlin", "rarity": "Epic", "weight": 2, "reward": 52},

    # 🔴 Legendary
    {"name": "Ancient Leviathan Scale", "rarity": "Legendary", "weight": 1, "reward": 100},
    {"name": "Abyssal Kraken Tentacle", "rarity": "Legendary", "weight": 1, "reward": 120},
    {"name": "Phantom Seahorse", "rarity": "Legendary", "weight": 1, "reward": 90},
    {"name": "Mythic Coral Wyrm", "rarity": "Legendary", "weight": 1, "reward": 150},
    {"name": "Celestial Bubblefish", "rarity": "Legendary", "weight": 1, "reward": 130},
    {"name": "Tideglass Leviathan", "rarity": "Legendary", "weight": 1, "reward": 110},

    # 🟡 Mythical
    {"name": "Astral Serpent", "rarity": "Mythical", "weight": 0.3, "reward": 250},
    {"name": "Chrono Carp", "rarity": "Mythical", "weight": 0.2, "reward": 300},
    {"name": "Starwhale Fragment", "rarity": "Mythical", "weight": 0.1, "reward": 400},
]

# 🎣 Bait Effects on Rarity Weights
BaitEffects = {
    "Worm Bait":    {"Common": 1.0, "Uncommon": 1.0, "Rare": 1.0, "Epic": 1.0, "Legendary": 1.0, "Mythical": 1.0},
    "Rock Bait":    {"Common": 1.3, "Uncommon": 0.9, "Rare": 0.8, "Epic": 0.5, "Legendary": 0.3, "Mythical": 0.1},
    "Salt Bait":    {"Common": 0.8, "Uncommon": 1.3, "Rare": 1.2, "Epic": 1.2, "Legendary": 1.1, "Mythical": 1.1},
    "Golden Bait":  {"Common": 0.5, "Uncommon": 0.8, "Rare": 1.1, "Epic": 1.5, "Legendary": 2.0, "Mythical": 3.0},
}
