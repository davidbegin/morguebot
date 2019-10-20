WEAPON_STATS = {
    "long sword": {"base_damage": 9, "hit_modifier": 1, "type": "long blades"},
    "short sword": {"base_damage": 6, "hit_modifier": 4, "type": "short blades"},
}


def max_damage(weapon_info):
    weapon_stats = WEAPON_STATS[weapon_info["type"]]
    base_damage = weapon_stats["base_damage"]
    return base_damage + weapon_info["modifier"]
    # {"type": "long sword", "modifier": "+9"},

# Damage = {[1d(Base damage * Strength modifier +1)-1] * Weapon skill modifier * Fighting modifier + Misc modifiers + Slaying bonuses} * Final multipliers + Stabbing bonus - AC damage reduction[1]
