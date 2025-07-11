# fish_data.py

# 🎏 Vast Pool of Fontaine's Finned Folk + many new additions + Treasure
FishPool = [
    # 🟢 Common (MORE!)
    {"name": "Salmon", "rarity": "Common", "weight": 50, "reward": 5},
    {"name": "Cod", "rarity": "Common", "weight": 50, "reward": 3},
    {"name": "Mackerel", "rarity": "Common", "weight": 40, "reward": 4},
    {"name": "Anchovy", "rarity": "Common", "weight": 45, "reward": 2},
    {"name": "Herring", "rarity": "Common", "weight": 40, "reward": 3},
    {"name": "Bubble Minnow", "rarity": "Common", "weight": 38, "reward": 2},
    {"name": "Drift Carp", "rarity": "Common", "weight": 35, "reward": 3},
    {"name": "Reed Perch", "rarity": "Common", "weight": 37, "reward": 4},
    {"name": "Pebble Goby", "rarity": "Common", "weight": 36, "reward": 3},
    {"name": "Creek Loach", "rarity": "Common", "weight": 34, "reward": 3},
    {"name": "Rusty Sunfish", "rarity": "Common", "weight": 33, "reward": 2},
    {"name": "Mud Skipper", "rarity": "Common", "weight": 32, "reward": 2},
    {"name": "Weedy Stickleback", "rarity": "Common", "weight": 31, "reward": 2},

    # 🔵 Uncommon (MORE!)
    {"name": "Tuna", "rarity": "Uncommon", "weight": 20, "reward": 8},
    {"name": "Sardine Swarm", "rarity": "Uncommon", "weight": 20, "reward": 7},
    {"name": "Sea Bass", "rarity": "Uncommon", "weight": 18, "reward": 9},
    {"name": "Glass Snapper", "rarity": "Uncommon", "weight": 16, "reward": 10},
    {"name": "Dusky Grunt", "rarity": "Uncommon", "weight": 15, "reward": 11},
    {"name": "Velvet Tetra", "rarity": "Uncommon", "weight": 14, "reward": 10},
    {"name": "Striped Drum", "rarity": "Uncommon", "weight": 13, "reward": 12},
    {"name": "Crimson Barb", "rarity": "Uncommon", "weight": 12, "reward": 12},
    {"name": "Bluefin Scad", "rarity": "Uncommon", "weight": 12, "reward": 11},

    # 🟣 Rare (MORE!)
    {"name": "Golden Carp", "rarity": "Rare", "weight": 10, "reward": 20},
    {"name": "Electric Eel", "rarity": "Rare", "weight": 10, "reward": 22},
    {"name": "Moon Jellyfish", "rarity": "Rare", "weight": 8, "reward": 18},
    {"name": "Stormfin Tuna", "rarity": "Rare", "weight": 7, "reward": 25},
    {"name": "Twilight Piranha", "rarity": "Rare", "weight": 6, "reward": 24},
    {"name": "Blazing Guppy", "rarity": "Rare", "weight": 6, "reward": 26},
    {"name": "Obsidian Catfish", "rarity": "Rare", "weight": 5, "reward": 28},
    {"name": "Whispering Grouper", "rarity": "Rare", "weight": 5, "reward": 27},

    # 🟠 Epic (MORE!)
    {"name": "Swordfish", "rarity": "Epic", "weight": 5, "reward": 40},
    {"name": "Ornamental Koi", "rarity": "Epic", "weight": 4, "reward": 35},
    {"name": "Crystal Lionfish", "rarity": "Epic", "weight": 3, "reward": 50},
    {"name": "Echo Stingray", "rarity": "Epic", "weight": 2, "reward": 55},
    {"name": "Frost Pike", "rarity": "Epic", "weight": 2, "reward": 48},
    {"name": "Aetherfin Marlin", "rarity": "Epic", "weight": 2, "reward": 52},
    {"name": "Runestone Ray", "rarity": "Epic", "weight": 1.5, "reward": 60},
    {"name": "Voidfin Swordtail", "rarity": "Epic", "weight": 1.2, "reward": 65},

    # 🔴 Legendary
    {"name": "Ancient Leviathan Scale", "rarity": "Legendary", "weight": 1, "reward": 100},
    {"name": "Abyssal Kraken Tentacle", "rarity": "Legendary", "weight": 1, "reward": 120},
    {"name": "Phantom Seahorse", "rarity": "Legendary", "weight": 1, "reward": 90},
    {"name": "Mythic Coral Wyrm", "rarity": "Legendary", "weight": 1, "reward": 150},
    {"name": "Celestial Bubblefish", "rarity": "Legendary", "weight": 1, "reward": 130},
    {"name": "Tideglass Leviathan", "rarity": "Legendary", "weight": 1, "reward": 110},
    {"name": "Eclipse Angler", "rarity": "Legendary", "weight": 1, "reward": 140},

    # 🟡 Mythical
    {"name": "Astral Serpent", "rarity": "Mythical", "weight": 0.3, "reward": 250},
    {"name": "Chrono Carp", "rarity": "Mythical", "weight": 0.2, "reward": 300},
    {"name": "Starwhale Fragment", "rarity": "Mythical", "weight": 0.1, "reward": 400},
    {"name": "Infinity Lanternfish", "rarity": "Mythical", "weight": 0.1, "reward": 500},

    # ✨ Treasure
    {"name": "Ancient Pearl", "rarity": "Treasure", "weight": 0.05, "reward": 900},
    {"name": "Lost King’s Crown", "rarity": "Treasure", "weight": 0.02, "reward": 1050},
    {"name": "Sunken Map Fragment", "rarity": "Treasure", "weight": 0.03, "reward": 950},
    {"name": "Enchanted Compass", "rarity": "Treasure", "weight": 0.02, "reward": 1150}
]

BaitEffects = {
    "Worm Bait":    {"Common": 1.0, "Uncommon": 1.0, "Rare": 1.0, "Epic": 1.0, "Legendary": 1.0, "Mythical": 1.0, "Treasure": 1.0},
    "Rock Bait":    {"Common": 1.3, "Uncommon": 0.9, "Rare": 0.8, "Epic": 0.5, "Legendary": 0.3, "Mythical": 0.1, "Treasure": 0.05},
    "Salt Bait":    {"Common": 0.8, "Uncommon": 1.3, "Rare": 1.2, "Epic": 1.2, "Legendary": 1.1, "Mythical": 1.1, "Treasure": 0.5},
    "Golden Bait":  {"Common": 0.5, "Uncommon": 0.8, "Rare": 1.1, "Epic": 1.5, "Legendary": 2.0, "Mythical": 3.0, "Treasure": 2.0},
}

FishingLocations = {
    "Crystal Shoals": {
        "description": "Vast waters, good balance.",
        "modifiers": {
            "Common": 1.2,
            "Uncommon": 1.1,
            "Rare": 0.9,
            "Epic": 0.7,
            "Legendary": 0.5,
            "Mythical": 0.2,
            "Treasure": 0.05
        },
        "min_exp": 0
    },
    "Midnight Trench": {
        "description": "Rich in Rare & Epic fish.",
        "modifiers": {
            "Common": 0.6,
            "Uncommon": 1.0,
            "Rare": 1.3,
            "Epic": 1.2,
            "Legendary": 1.0,
            "Mythical": 0.4,
            "Treasure": 0.3
        },
        "min_exp": 8
    },
    "Frostbite Cove": {
        "description": "Icy cove with chilling waters; epic and rare fish brave the cold.",
        "modifiers": {
            "Common": 0.4,
            "Uncommon": 0.9,
            "Rare": 1.5,
            "Epic": 1.7,
            "Legendary": 1.8,
            "Mythical": 1.5,
            "Treasure": 1.2
        },
        "min_exp": 19
    },
    # New Locations unlocked by experience
    "Crystal Lagoon": {
        "description": "Shimmering waters where Mythical fish dwell, shimmering like stars.",
        "modifiers": {
            "Common": 0.3,
            "Uncommon": 0.7,
            "Rare": 1.0,
            "Epic": 1.2,
            "Legendary": 1.5,
            "Mythical": 2.5,
            "Treasure": 1.0
        },
        "min_exp": 32
    },
    "Ethereal Spire": {
        "description": "Deep & dangerous... Legendary odds boosted!",
        "modifiers": {
            "Common": 0.1,
            "Uncommon": 0.5,
            "Rare": 0.8,
            "Epic": 1.5,
            "Legendary": 2.0,
            "Mythical": 3.0,
            "Treasure": 2.0
        },
        "min_exp": 43
    },
    
    "Sunken Ruins": {
        "description": "Ancient ruins beneath the waves, home to rare treasures and fish of legend.",
        "modifiers": {
            "Common": 0.2,
            "Uncommon": 0.8,
            "Rare": 1.4,
            "Epic": 1.6,
            "Legendary": 2.2,
            "Mythical": 2.0,
            "Treasure": 3.0
        },
        "min_exp": 58
    }

}
