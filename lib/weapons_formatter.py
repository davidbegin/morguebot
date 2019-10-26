import re
import random

from lib.morgue_parser import fetch_skill
from lib.morgue_parser import fetch_strength
from lib.morgue_parser import fetch_weapon
from lib.morgue_parser import fetch_weapons
from lib.weapon_stats import WEAPON_STATS
from lib.weapons_appraiser import WeaponsAppraiser


class WeaponsFormatter:
    def __init__(self, character, weapons):
        self.character = character
        self.character_name = character.name
        self.weapons = weapons

    def format_max_damages(self):
        weapons_appraiser = WeaponsAppraiser(
            character=self.character, weapons=self.weapons
        )
        max_damages = weapons_appraiser.calc_max_damages()

        formatted_max_damages = []

        for weapon_info in max_damages:
            formatted_weapon = self.format_weapon(weapon_info)
            formatted_max_damages.append(formatted_weapon)

        # Why don't these strings match
        if "(weapon)" in max_damages[-1]["weapon"]:
            extra_msg = [
                "CoolCat Noice you are using your highest Damage Weapon! CoolCat"
            ]
        else:
            strongest_weapon = formatted_max_damages.pop()
            formatted_max_damages.append(f"VoteYea {strongest_weapon}")
            extra_msg = [
                "PixelBob Hey why aren't you using your best weapon??? PixelBob"
            ]
        return formatted_max_damages + extra_msg

    def format_weapon(self, weapon_info):
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
            return f"riPepperonis {weapon.replace('(weapon)', '')} {emote_l} Max Damage: {raw_max_damage} {emote_r}"
        else:
            return f"{weapon} {emote_l} Max Damage: {raw_max_damage} {emote_r}"
