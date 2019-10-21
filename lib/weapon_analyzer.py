import re
import random

from lib.morgue_parser import fetch_skill
from lib.morgue_parser import fetch_strength
from lib.morgue_parser import fetch_weapon
from lib.morgue_parser import fetch_weapons
from lib.item_parser import parse_weapon
from lib.weapon_stats import WEAPON_STATS
from lib.damage_calculator import calc_max_damage


class MaxDamageCalculator:
    def __init__(self, character):
        self.character = character
        self.character_name = character.character
        self.morgue_file = character.morgue_file()
        self.wielded_weapon = fetch_weapon(self.morgue_file)
        self.weapons = fetch_weapons(self.morgue_file)

    def max_damage(self):
        if len(self.weapons) == 0:
            return ["No Weapons Found!"]

        max_damages = self._find_max_damages()

        if len(max_damages) > 0:
            return max_damages
            # return format_max_damages(max_damages, wielded_weapon)

    def _find_max_damages(self):
        max_damages = []
        for weapon in self.weapons:
            weapon_info = parse_weapon(weapon)
            if weapon_info:
                max_damage = calc_max_damage(weapon_info, self.morgue_file)
                max_damages.append(
                    {
                        "weapon": weapon,
                        "max_damage": max_damage,
                        "type": weapon_info["type"],
                        "character": self.character_name,
                    }
                )
            else:
                print(f"\033[33mNo Weapon Info For: {weapon}\033[0m")

        def sort_by_max_damage(elem):
            return elem["max_damage"]

        max_damages.sort(key=sort_by_max_damage)

        return max_damages

    def format_max_damages(self, max_damages):
        if max_damages[-1]["weapon"] == self.wielded_weapon:
            extra_msg = [
                "CoolCat Noice you are using your highest Damage Weapon! CoolCat"
            ]
        else:
            extra_msg = [
                "PixelBob Hey why aren't you using your best weapon??? PixelBob"
            ]

        formatted_max_damages = []

        for weapon_info in max_damages:
            raw_max_damage = weapon_info["max_damage"]
            weapon = weapon_info["weapon"]

            if raw_max_damage >= 100:
                emote_l, emote_r = (
                    "PowerUpL PowerUpL PowerUpL",
                    "PowerUpR PowerUpR PowerUpR",
                )
            elif raw_max_damage > 80:
                emote_l, emote_r = "PowerUpL PowerUpL", "PowerUpR PowerUpR"
            elif raw_max_damage > 40:
                emote_l, emote_r = "PowerUpL", "PowerUpR"
            else:
                emote_l, emote_r = "-", ""

            if "(weapon)" in weapon:
                formatted_max_damages.append(
                    f"riPepperonis {weapon.replace('(weapon)', '')} {emote_l} Max Damage: {raw_max_damage} {emote_r}"
                )
            elif weapon == max_damages[-1]["weapon"]:
                formatted_max_damages.append(
                    f"VoteYea {weapon} {emote_l} Max Damage: {raw_max_damage} {emote_r}"
                )
            else:
                formatted_max_damages.append(
                    f"{weapon} {emote_l} Max Damage: {raw_max_damage} {emote_r}"
                )
        return formatted_max_damages + extra_msg
