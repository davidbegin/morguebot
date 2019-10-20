WEAPON_STATS = {
    "long sword": {"base_damage": 9, "hit_modifier": 1, "type": "long blades"},
    "short sword": {"base_damage": 6, "hit_modifier": 4, "type": "short blades"},
}


# {"type": "long sword", "modifier": "+9"},
def max_damage(character, weapon_info):
    base_damage = calc_base_damage(weapon_info, weapon_stats)
    strength_modifier = calc_strength_modifier(character)

    return base_damage + weapon_info["modifier"]
    # Damage = {[1d(Base damage * Strength modifier +1)-1] * Weapon skill modifier * Fighting modifier + Misc modifiers + Slaying bonuses}


# Base damage:
# Unarmed combat: 3 + UC (can be changed by some spells, see Unarmed combat)
# Using a weapon: Base damage of the weapon
def calc_base_damage(weapon_info, weapon_stats):
    return weapon_stats["base_damage"]


# Strength modifier:
# If Strength > 10: (39+((1d(Strength-8)-1)*2))/39
# If Strength < 10: (39-((1d(12-Strength)-1)*3))/39
# If Strength = 10: 1
def calc_strength_modifier():
    pass


# Weapon skill modifier: Multiply by [2499 + 1d(100 * weapon_skill +1)]/2500 (not applied to unarmed combat)
# Fighting modifier: Multiply by [3999 + 1d(100 * fighting_skill +1)]/4000
def calc_fighting_modifier():
    pass


# Misc modifiers:
# Might or Berserk: +1d10
# If you are starving: -1d5 + 1 (bloodless vampires don't suffer this penalty)
def calc_misc_modifier():
    pass


# Slaying bonuses:
# Effective enchantment = Weapon enchantment + Slaying bonus
# If Eff. enchantment > 0: + 1d(1 + Eff. enchantment) - 1
# If Eff. enchantment < 0: - 1d(1 - Eff. enchantment) + 1
def calc_slay_bonuses():
    pass


# Final multipliers:
# If it is an additional cleaving attack: Multiply by 0.7
# Statue Form: Multiply by 1.5
# Shadow Form: Multiply by 0.5
# If the player has the Weak status effect: Multiply by 0.75
def calc_final_multipliers():
    pass


# Stabbing bonus: See stabbing.
def calc_stabbing_bonus():
    pass


# AC damage reduction: See AC.
def calc_ac_damage_reduction():
    pass


# Damage = {[1d(Base damage * Strength modifier +1)-1] * Weapon skill modifier * Fighting modifier + Misc modifiers + Slaying bonuses} * Final multipliers + Stabbing bonus - AC damage reduction[1]
