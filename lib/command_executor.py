import os
import boto3
import re
import time

from lib.character import Character
from lib.kinesis import send_chat_to_stream
from lib.morgue_saver import morgue_saver
from lib.config import find_character_name
from lib.weapon_awards import find_the_max_damage_for_all_characters
from lib.rune_awards import rune_awards
from lib.rune_fetcher import RuneFetcher
from lib.morgue_stalker import fetch_characters
from lib.help import WORKING_COMMANDS
from lib.morgue_event import COMMANDS
from lib.morgue_event import MorgueEvent

from lib.weapons_formatter import WeaponsFormatter

from lib.the_real_morgue_parser import MorgueParser


def print_the_help(logger):
    # Flattening List
    # msg = [item for sublist in nested_msg for item in sublist]
    commands = [item for sublist in COMMANDS.values() for item in sublist]
    help_msgs = [
        "TheIlluminati Some Valid Commands: TheIlluminati",
        ", ".join(commands),
    ]
    send_chat_to_stream(help_msgs)


def process_event(event):
    morgue_event = MorgueEvent.from_event(event)

    if morgue_event.command == "!h?":
        return print_the_help()

    # Elif Island
    msg = None
    if morgue_event.is_character_command():
        print("A single Character Command!")
        character = Character(name=morgue_event.character)
        formatter = Formatter(character)

        if morgue_event.command == "!armour":
            msg = formatter.print_armour()
        elif morgue_event.command == "!weapons":
            msg = formatter.print_weapons()
        elif morgue_event.command == "!runes":
            msg = formatter.print_runes()
        elif morgue_event.command == "!spells":

            if morgue_event.level_barrier:
                msg = character.spells_above(morgue_event.level_barrier)
            else:
                msg = formatter.print_spells()

        elif morgue_event.command == "!skills":
            msg = formatter.print_skills()
        elif morgue_event.command == "!version":
            msg = formatter.print_version()
        elif morgue_event.command == "!jewellery":
            msg = formatter.print_jewellery()
            print(f"WE are looking for jewellery and this is what we found {msg}")
        elif morgue_event.command == "!max_damage":
            msg = formatter.print_max_damage()
        elif morgue_event.command == "!mutations":
            msg = formatter.print_mutations()
        elif morgue_event.command == "!scrolls":
            msg = formatter.print_scrolls()
        elif morgue_event.command == "!potions":
            msg = formatter.print_potions()
        elif morgue_event.command == "!gods":
            msg = formatter.print_gods()
        elif morgue_event.command == "!overview":
            morgue_parser = MorgueParser(character.non_saved_morgue_file())
            msg = morgue_parser.overview()
        elif morgue_event.command == "!fetch":
            morgue_saver(character, character.non_saved_morgue_file(), True)
        elif morgue_event.command == "!fetch_s3_morgue":
            print(f"We are fetching the S3 Morgue for {character.name}")
            with open(f"tmp/s3_{character.name}.txt", "w") as f:
                f.write(character.s3_morgue_file())
        elif morgue_event.command == "!save_morgue":
            save_morgue(character)
        elif morgue_event.command == "!search":
            pass
            # for c in ["!armour", "!weapons", "!jewellery"]:
            #     call_command_with_arg(formatter, c, morgue_event.args[0])

    elif morgue_event.is_multi_character_command():
        print("A multiple Character Command!")
        if morgue_event.command == "!stalk_all":
            characters = fetch_characters()
            for character in characters:
                character = Character(name=character)
                morgue_saver(character, character.non_saved_morgue_file(), True)
        elif morgue_event.command == "!rune_awards":
            rune_awards()
        elif morgue_event.command == "!characters":
            characters = fetch_characters()
            msg = ["All The Characters"] + [", ".join(characters)]
        elif morgue_event.command == "!clean_morgue":
            print("COMING SOON")
            # clean_the_morgue()
        elif morgue_event.command == "!weapon_awards":
            find_the_max_damage_for_all_characters()
    else:
        print("WE DON'T KNOW THAT COMMAND!!!!!!!")

    if morgue_event.search:
        print(f"We are searching: {morgue_event.search}")

        if type(msg) is list:
            print("Search a List")
            msg = [item for item in msg if morgue_event.search in item]
        else:
            print("Search a strang")
            if morgue_event.search not in msg:
                msg = None

    if msg:
        send_chat_to_stream(msg)
    else:
        print(
            f"No Message return for command: {morgue_event.command} character: {morgue_event.character}"
        )


def save_morgue(character):
    f = character.non_saved_morgue_file()
    os.makedirs("tmp", exist_ok=True)
    with open(f"tmp/{character.name}_morguefile.txt", "w") as morguefile:
        morguefile.write(f)


class Formatter:
    def __init__(self, character=None):
        self.character = character
        self.morgue_parser = MorgueParser(self.character.morgue_file())

    def print_command(self, name, value):
        fmt_str = f"{name}: {value}"
        print("\n\033[35m" + fmt_str + "\033[0m")
        return [fmt_str]

    def print_gods(self):
        gods = self.morgue_parser.gods()
        gods_remaining = 25 - len(gods)

        if len(gods) == 25:
            return ["Kreygasm YOU HAVE SEEN EVERY GOD! Kreygasm"]
        else:
            return [
                f"MercyWing1 Gods MercyWing2",
                ", ".join(sorted(gods)),
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

    def print_mutations(self):
        title = [f"Squid1 Squid2 Listing All Mutations Squid4"]
        return title + [self.morgue_parser.mutations()]

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
        weapons = self.morgue_parser.weapons()
        # weapons = self.find_unique_items(raw_weapons, "\w\s-\s(.*)")
        if weapons:
            return ["twitchRaid Listing All Weapons twitchRaid"] + weapons
        else:
            return ["No Weapons Found!"]

    def print_armour(self):
        armour = self.morgue_parser.armour()
        if armour:
            return ["BloodTrail Listing All Armour BloodTrail"] + armour
        else:
            return ["No Armour Found!"]

    def print_jewellery(self):
        jewellery = self.morgue_parser.jewellery()
        if jewellery:
            return ["CoolCat Listing All Jewellery CoolCat"] + jewellery
        else:
            return ["No Jewellery Found!"]

    def print_potions(self):
        potions = self.morgue_parser.potions()

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
        scrolls = self.morgue_parser.scrolls()

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
        weapons = self.morgue_parser.weapons()
        return WeaponsFormatter(
            character=self.character, weapons=weapons
        ).format_max_damages()
