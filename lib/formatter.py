import boto3
import os
import re
import time

from lib.morgue_parser import fetch_overview
from lib.morgue_parser import fetch_mutations
from lib.morgue_parser import fetch_jewellery
from lib.morgue_parser import fetch_scrolls
from lib.morgue_parser import fetch_potions
from lib.morgue_parser import fetch_weapons
from lib.morgue_parser import fetch_armour
from lib.morgue_parser import fetch_skills
from lib.morgue_parser import fetch_altars
from lib.morgue_parser import fetch_weapon

from lib.the_real_morgue_parser import MorgueParser


from lib.character import Character

from lib.weapons_formatter import WeaponsFormatter


class Formatter:
    def __init__(self, character=None):
        self.character = character
        self.morgue_parser = MorgueParser(self.character.morgue_file())

    def construct_message(self, command):
        print(f"Formatter construct_message {command} for {self.character.name}")

        if command == "!overview":
            return self.print_overview()
        elif command == "!weapons":
            return self.print_weapons()
        elif command == "!armour":
            return self.print_armour()
        elif command == "!jewellery":
            return self.print_jewellery()
        elif command == "!skills":
            return self.print_skills()
        elif command == "!mutations":
            return self.print_mutations()
        elif command == "!potions":
            return self.print_potions()
        elif command == "!runes":
            return self.print_runes()
        elif command == "!scrolls":
            return self.print_scrolls()
        elif command == "!spells":
            return self.print_spells()
        elif command == "!version":
            return self.print_version()
        elif command == "!max_damage":
            return self.print_max_damage()

    def print_command(self, name, value):
        fmt_str = f"{name}: {value}"
        print("\n\033[35m" + fmt_str + "\033[0m")
        return [fmt_str]

    def print_gods(self, morgue_file):
        altars = set(fetch_altars(morgue_file))
        gods_remaining = 25 - len(altars)

        if len(altars) == 25:
            return ["Kreygasm YOU HAVE SEEN EVERY GOD! Kreygasm"]
        else:
            return [
                f"MercyWing1 Gods MercyWing2",
                ", ".join(sorted(altars)),
                f"You have {gods_remaining} to be found",
            ]

    def print_spells(self):
        morgue_parser = MorgueParser(self.character.morgue_file())
        raw_spells = morgue_parser.spells()
        spells = [spell for spell in raw_spells if (len(spell.split()) >= 5)]
        formatted_spells = []
        for spell in spells:
            spell_parts = spell.split()
            spell_parts.reverse()
            hunger, level, failure, power, spell_type, *spell = spell_parts
            formatted_spells.append(
                f"{' '.join(spell)} - {spell_type} - {power} - {failure}"
            )

        return [
            "TakeNRG Listing All Spells TakeNRG",
            "Spell Type Power Failure",
        ] + formatted_spells

    def print_skills(self):
        skills = fetch_skills(self.character.morgue_file())

        formatted_skills = []
        for skill in skills:
            split_skills = skill.split()
            if len(split_skills) == 3:
                _, level, *skill = skill.split()
            else:
                _, _, level, *skill = skill.split()

            formatted_skills.append(f"Level {level} {' '.join(skill)}")

        return ["PowerUpL Listing All Skills PowerUpR"] + formatted_skills

    # ========================================================================================

    def print_version(self):
        return self.character.morgue_file().split("\n")[0]

    def print_overview(self):
        overview = fetch_overview(self.character.morgue_file())
        print("\n\033[35m" + str(overview) + "\033[0m")
        return overview

    def print_mutations(self):
        return [f"Squid1 Squid2 Listing All Mutations Squid4"] + self.print_command(
            "Mutations", fetch_mutations(self.character.morgue_file())
        )

    # ========================================================================================

    def find_unique_items(self, items, regex):
        if items is None:
            return None

        uniq_items = []
        for item in items:
            m = re.search(regex, item)
            if m:
                # This should check for the amout of groups to know whether it has amounts
                msg = m.group(1)
                uniq_items.append(m.group(1))

        return uniq_items

    def print_runes(self):
        return self.morgue_parser.runes()

    def print_weapons(self):
        weapons = fetch_weapons(self.character.morgue_file())
        # weapons = self.find_unique_items(raw_weapons, "\w\s-\s(.*)")
        if weapons:
            return ["twitchRaid Listing All Weapons twitchRaid"] + weapons
        else:
            return ["No Weapons Found!"]

    def print_armour(self):
        armour = self.find_unique_items(
            fetch_armour(self.character.morgue_file()), "\w\s-\s(.*)"
        )
        if armour:
            return ["BloodTrail Listing All Armour BloodTrail"] + armour
        else:
            return ["No Armour Found!"]

    def print_jewellery(self):
        jewellery = self.find_unique_items(
            fetch_jewellery(self.character.morgue_file()), "\w\s-\s(.*)"
        )
        if jewellery:
            return ["CoolCat Listing All Jewellery CoolCat"] + jewellery
        else:
            return ["No Jewellery Found!"]

    def print_potions(self):
        potions = fetch_potions(self.character.morgue_file())

        formatted_potions = []
        for potion in potions:
            m = re.search(f"\w\s-\s(\d+)\s(.*)", potion)
            if m:
                amount = m.group(1)
                potion_name = m.group(2)
                msg = f"{amount} {potion_name}"
                print(msg)

                formatted_potions.append(msg)

        return [f"DrinkPurple Listing All Potions DrinkPurple"] + formatted_potions

    def print_scrolls(self):
        scrolls = fetch_scrolls(self.character.morgue_file())

        formatted_scrolls = []
        for scroll in scrolls:
            m = re.search(f"\w\s-\s(\d+)\s(.*)", scroll)
            if m:
                amount = m.group(1)
                scroll_name = m.group(2)
                msg = f"{amount} {scroll_name}"
                print(msg)
                formatted_scrolls.append(msg)

        return ["copyThis Listing All Scrolls copyThis"] + formatted_scrolls

    # ========================================================================================

    def print_max_damage(self):
        if True:
            weapons = fetch_weapons(self.character.morgue_file())
            return WeaponsFormatter(
                character=self.character, weapons=weapons
            ).format_max_damages()
        else:
            max_damages = {}
            from morgue_stalker import fetch_characters

            characters = morgue_stalker.fetch_characters()

            for character in characters:
                max_damages[character] = max_damage(
                    Character(name=character).morgue_file()
                )
            return max_damages
