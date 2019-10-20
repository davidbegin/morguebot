import re
import random

from lib.dice import one_d

from lib.morgue_parser import fetch_skill
from lib.morgue_parser import fetch_strength
from lib.morgue_parser import fetch_weapon
from lib.morgue_parser import fetch_weapons
from lib.item_parser import parse_weapon
from lib.weapon_stats import WEAPON_STATS

# Damage = {[1d(Base damage * Strength modifier +1)-1] * Weapon skill modifier * Fighting modifier + Misc modifiers + Slaying bonuses} * Final multipliers + Stabbing bonus - AC damage reduction[1]
def calc_max_damage(weapon, morgue_file):
    weapon_info = parse_weapon(weapon)
    base_damage = calc_base_damage(weapon_info["name"])

    strength = fetch_strength(morgue_file)
    strength_modifier = calc_strength_modifier(strength)

    weapon_stats = WEAPON_STATS[weapon_info["name"]]
    weapon_type = weapon_stats["type"]
    weapon_skill = fetch_skill(morgue_file, weapon_type)
    weapon_skill_modifier = calc_weapon_skill_modifier(weapon_skill)

    fighting_skill = fetch_skill(morgue_file, "Fighting")
    fighting_skill_modifier = calc_fighting_modifier(fighting_skill)

    slaying_bonuses = calc_slay_bonuses(weapon_info["modifier"])

    misc_modifiers = 0

    base_damage + weapon_info["modifier"] + strength_modifier

    max_damage = (
        (one_d(base_damage * strength_modifier + 1) - 1)
        * weapon_skill_modifier
        * fighting_skill_modifier
        + misc_modifiers
        + slaying_bonuses
    )

    return round(max_damage, 2)


def max_damage(morgue_file):
    weapon = fetch_weapon(morgue_file)
    weapons = fetch_weapons(morgue_file)

    max_damages = [
        {"weapon": weapon, "max_damage": calc_max_damage(weapon, morgue_file)}
        for weapon in weapons
    ]

    def sort_by_max_damage(elem):
        return elem["max_damage"]

    max_damages.sort(key=sort_by_max_damage)

    if max_damages[-1]["weapon"] == weapon:
        print("nice you are using your best weapon")
        extra_msg = []
    else:
        extra_msg = ["PixelBob Hey why aren't you using your best weapon??? PixelBob"]

    formatted_max_damages = []

    for weapon_info in max_damages:
        raw_max_damage = weapon_info["max_damage"]
        weapon = weapon_info["weapon"]

        if raw_max_damage > 40:
            emote_l, emote_r = "PowerUpL", "PowerUpR"
        else:
            emote_l, emote_r = "-", ""

        formatted_max_damages.append(
            f"{weapon} {emote_l} Max Damage: {raw_max_damage} {emote_r}"
        )
    return formatted_max_damages + extra_msg


# Base damage:
# Unarmed combat: 3 + UC (can be changed by some spells, see Unarmed combat)
# Using a weapon: Base damage of the weapon
# TODO: come back handle these no weapon jerks
def calc_base_damage(weapon_type):
    if weapon_type in WEAPON_STATS:
        return WEAPON_STATS[weapon_type]["base_damage"]
    else:
        raise Exception(f"\033[31;1mUnknown Weapon: {weapon_type}\033[0m")


# Strength modifier:
# If Strength > 10: (39+((1d(Strength-8)-1)*2))/39
# If Strength < 10: (39-((1d(12-Strength)-1)*3))/39
# If Strength = 10: 1
def calc_strength_modifier(strength):
    if strength == 10:
        return 1
    if strength > 10:
        return (39 + ((one_d(strength - 8) - 1) * 2)) / 39
    elif strength < 10:
        return (39 - ((one_d(12 - strength) - 1) * 3)) / 39


# Weapon skill modifier: Multiply by [2499 + 1d(100 * weapon_skill +1)]/2500 (not applied to unarmed combat)
def calc_weapon_skill_modifier(weapon_skill):
    return (2499 + one_d(100 * weapon_skill + 1)) / 2500


# Fighting modifier: Multiply by [3999 + 1d(100 * fighting_skill +1)]/4000
def calc_fighting_modifier(fighting_skill):
    return (3999 + one_d(100 * fighting_skill + 1)) / 4000


# Misc modifiers:
# Might or Berserk: +1d10
# If you are starving: -1d5 + 1 (bloodless vampires don't suffer this penalty)
def calc_misc_modifier():
    return 0


# Slaying bonuses:
# Effective enchantment = Weapon enchantment + Slaying bonus
# If Eff. enchantment > 0: + 1d(1 + Eff. enchantment) - 1
# If Eff. enchantment < 0: - 1d(1 - Eff. enchantment) + 1
def calc_slay_bonuses(enchantment):
    eff_enchantment = enchantment + 0

    if eff_enchantment > 0:
        return one_d(1 + eff_enchantment) - 1
    elif enchantment < 0:
        return -(one_d(1 - eff_enchantment) + 1)
    else:
        return 0


# Final multipliers:
# If it is an additional cleaving attack: Multiply by 0.7
# Statue Form: Multiply by 1.5
# Shadow Form: Multiply by 0.5
# If the player has the Weak status effect: Multiply by 0.75
def calc_final_multipliers():
    return 0


# Stabbing bonus: See stabbing.
def calc_stabbing_bonus():
    return 0


# AC damage reduction: See AC.
def calc_ac_damage_reduction():
    return 0
