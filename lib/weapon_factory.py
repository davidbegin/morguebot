import re

from lib.weapon_stats import WEAPON_STATS
from lib.weapon import Weapon


class UnidentifiedWeapon:
    def __init__(self, name):
        self.name = name
        self.full_name = name
        self.weapon_type = "Unknown"

    def max_damage(self):
        return 0


class WeaponFactory:
    @staticmethod
    def new(character, raw_weapon):
        m = re.search(f"([-+]\d+)(.*)", raw_weapon)
        enchantment = None

        if m:
            raw_enchantment = m.group(1).strip()

            if raw_enchantment.startswith("+"):
                enchantment = int(raw_enchantment[1:])
            else:
                enchantment = int(raw_enchantment)

            rest_of_the_weapon = m.group(2)
            weapon_name = WeaponFactory.find_weapon_name(rest_of_the_weapon)

            return Weapon(
                full_name=raw_weapon,
                name=weapon_name,
                enchantment=enchantment,
                character=character,
            )
        else:
            print(f"\033[31;1mError Building a Weapon: {raw_weapon}\033[0m")
            return UnidentifiedWeapon(name=raw_weapon)

    @staticmethod
    def find_weapon_name(rest_of_the_weapon):
        rest_of_the_weapon = rest_of_the_weapon.lower()
        weapon_name = None

        for weapon in WEAPON_STATS.keys():
            if weapon in rest_of_the_weapon:
                weapon_name = weapon

        if weapon_name is None:
            if "sword" in rest_of_the_weapon:
                weapon_name = "long sword"
            elif "katana" in rest_of_the_weapon:
                weapon_name = "long sword"
            elif "storm bow" in rest_of_the_weapon:
                weapon_name = "longbow"
            elif "lance" in rest_of_the_weapon:
                weapon_name = "spear"
            elif "maxwell's thermic engine" in rest_of_the_weapon:
                weapon_name = "double sword"
            elif "wrath of trog" in rest_of_the_weapon:
                weapon_name = "battleaxe"
            elif "heavy crossbow" in rest_of_the_weapon:
                weapon_name = "arbalest"
            elif "mithril axe" in rest_of_the_weapon:
                weapon_name = "broad axe"
            elif "arc blade" in rest_of_the_weapon:
                weapon_name = "rapier"
            elif "dark maul" in rest_of_the_weapon:
                weapon_name = "great mace"
            elif "majin-bo" in rest_of_the_weapon:
                weapon_name = "quarterstaff"
            elif "captain's cutlass" in rest_of_the_weapon:
                weapon_name = "rapier"
            elif "spriggan's knife" in rest_of_the_weapon:
                weapon_name = "dagger"
            elif "obsidian axe" in rest_of_the_weapon:
                weapon_name = "broad axe"
            elif "sceptre of torment" in rest_of_the_weapon:
                weapon_name = "eveningstar"
            elif 'sling "punk"':
                weapon_name = "fustibalus"

        return weapon_name
