import os
import re
import time
from lib.morgue_parser import fetch_overview
from lib.morgue_parser import fetch_resistance
from lib.morgue_parser import fetch_trait
from lib.morgue_parser import fetch_mr
from lib.morgue_parser import fetch_stealth
from lib.morgue_parser import fetch_mutations
from lib.morgue_parser import fetch_jewellery
from lib.morgue_parser import fetch_scrolls
from lib.morgue_parser import fetch_potions
from lib.morgue_parser import fetch_weapons
from lib.morgue_parser import fetch_armour
from lib.morgue_parser import fetch_skills
from lib.morgue_parser import fetch_spells
from lib.morgue_parser import fetch_altars


# I Need a better data struct for aliases
ALIASES = {"rF": "rFire", "rE": "rElec", "rC": "rCold", "rP": "rPois", "MR": "TODO"}

RESISTANCES = ["!rF", "!rFire", "!rCold", "!rNeg", "!rPois", "!rE", "!rElec", "!rCorr"]
TRAITS = ["!SeeInvis", "!Gourm", "!Faith", "!Spirit", "!Reflect", "!Harm"]

WORKING_COMMANDS = [
    "!overview",
    "!h?",
    "!weapons",
    "!armour",
    "!jewellery",
    "!skills",
    "!potions",
    "!scrolls",
    "!spells",
    "!version",
]

COMMANDS_WITH_NO_ARGS = (
    [
        "!overview",
        "!mr",
        "!stlth",
        "!mutations",
        "!jewellery",
        "!scrolls",
        "!potions",
        "!weapons",
        "!armour",
        "!skills",
        "!spells",
        "!h?",
        "!maxR",
        "!mf",
        "!gods",
    ]
    + RESISTANCES
    + TRAITS
)


class Formatter:
    def __init__(self, character=None):
        self.character = character

    def construct_message(self, command):
        print(f"Formatter construct_message {command} for {self.character.character}")

        if command == "!overview":
            return self.print_overview()
        elif command == "!h?":
            return self.print_help()
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
        elif command == "!scrolls":
            return self.print_scrolls()
        elif command == "!spells":
            return self.print_spells()
        elif command == "!version":
            return self.print_version()
        # elif command == "!stlth":
        #     self.print_stealth()
        # elif command == "!mr":
        #     return self.print_mr()
        # elif command == "!maxR":
        #     return self.print_max_resistance()
        # elif command == "!gods":
        #     return self.print_gods()
        # elif command == "!mf":
        #     pass
        # elif command in RESISTANCES:
        #     return self.print_resistance(command[1:])
        # elif command in TRAITS:
        #     return self.print_traits(command)

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
        raw_spells = fetch_spells(self.character.morgue_file())
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

    def print_stealth(self, morgue_file):
        return self.print_command("Stealth", fetch_stealth(morgue_file))

    def print_mr(self, morgue_file):
        return self.print_command("Magic Resistance", fetch_mr(morgue_file))

    # ========================================================================================

    def print_traits(self, trait_type, morgue_file):
        trait = fetch_trait(morgue_file, trait_type[1:])

        if trait:
            trait_str = f"{trait_type[1:]}:   {trait}"
            print("\n\033[35m" + trait_str + "\033[0m")
            return trait_str
        else:
            print("\n\033[35m" + "No TRAIT FOUND! " + "\033[0m")

    def print_resistance(self, resistance_type, morgue_file):
        if ALIASES.get(resistance_type, None):
            resistance = fetch_resistance(morgue_file, ALIASES[resistance_type])
        else:
            resistance = fetch_resistance(morgue_file, resistance_type)

        if resistance:
            resistance_str = f"{resistance_type}:   {resistance}"
            print("\n\033[35m" + resistance_str + "\033[0m")
            return resistance_str
        else:
            print("\n\033[35m" + "No Resistance FOUND! " + "\033[0m")

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

    def print_missionary(self, new_altars):
        return ["MercyWing1 New Gods! MercyWing2", ", ".join(new_altars)]

    def print_help(self):
        return [
            "TheIlluminati Valid Commands: TheIlluminati",
            ", ".join(WORKING_COMMANDS),
        ]

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

    def print_weapons(self):
        weapons = self.find_unique_items(
            fetch_weapons(self.character.morgue_file()), "\w\s-\s(.*)"
        )
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

    # ========================================================================================

    # TODO: combing the capture into, or branch on amout
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
