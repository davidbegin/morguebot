import os


from lib.character import Character
from lib.formatter import Formatter
from lib.kinesis import send_chat_to_stream
from lib.morgue_saver import morgue_saver
from lib.config import find_character_name
from lib.weapon_awards import find_the_max_damage_for_all_characters
from lib.rune_awards import rune_awards
from lib.the_real_morgue_parser import MorgueParser
from lib.rune_fetcher import RuneFetcher
from lib.morgue_stalker import fetch_characters
from lib.help import WORKING_COMMANDS


# An Event:
# {
#     "character",
#     "command",
#     "arg1",
#     "arg2",
# }
def process_event(event):
    command = event["command"]

    if command != "!h?":
        character_name = find_character_name(event)
        character = Character(name=character_name)
        formatter = Formatter(character)

    arg1 = event.get("arg1", None)
    arg2 = event.get("arg2", None)

    if command == "!h?":
        help_msgs = [
            "TheIlluminati Some Valid Commands: TheIlluminati",
            ", ".join(WORKING_COMMANDS),
        ]

        send_chat_to_stream(help_msgs)
    elif command == "!fetch":
        morgue_saver(character, character.non_saved_morgue_file(), arg1)
    if command == "!stalk_all":
        characters = fetch_characters()
        for character in characters:
            character = Character(name=character)
            morgue_saver(character, character.non_saved_morgue_file(), arg1)
    elif command == "!characters":
        characters = fetch_characters()
        send_chat_to_stream(["All The Characters"] + [", ".join(characters)])
    elif command == "!fetch_runes":
        RuneFetcher().fetch()
    elif command == "!fetch_s3_morgue":
        print(f"We are fetching the S3 Morgue for {character.name}")
        with open(f"tmp/s3_{character.name}.txt", "w") as f:
            f.write(character.s3_morgue_file())
    elif command == "!spells":
        print("We about to print some spells")

        if arg1 == "level":
            msg = character.spells_above(arg2)
            print(f"msg: {msg}")
            send_chat_to_stream(msg)
        else:
            print(f"Oh no arg1: {arg1}")

    elif command == "!overview":
        morgue_parser = MorgueParser(character.non_saved_morgue_file())
        msg = morgue_parser.overview()
        send_chat_to_stream(msg)
    elif command == "!save_morgue":
        save_morgue(character)
    elif command == "!clean_morgue":
        clean_the_morgue()
    elif command == "!rune_awards":
        rune_awards()
    elif command == "!weapon_awards":
        find_the_max_damage_for_all_characters()
    elif command == "!search":
        for c in ["!armour", "!weapons", "!jewellery"]:
            call_command_with_arg(formatter, c, arg1)
    elif arg1:
        print(f"\033[37;1marg1: {arg1}\033[0m")
        print(f"\033[37;1marg1 type: {type(arg1)}\033[0m")
        call_command_with_arg(formatter, command, arg1)
    else:
        call_command(formatter, command, character_name)


# ========================================================================================


def call_command(formatter, command, character_name):
    msg = formatter.construct_message(command)
    if msg:
        send_chat_to_stream(msg)
    else:
        print(f"No Message return for command: {command} character: {character_name}")


def call_command_with_arg(formatter, command, arg1):
    all_values = formatter.construct_message(command)
    filtered_values = [value for value in all_values if arg1 in value]
    if filtered_values:
        send_chat_to_stream([f"Result of your search for '{arg1}': "] + filtered_values)


def save_morgue(character):
    f = character.non_saved_morgue_file()
    os.makedirs("tmp", exist_ok=True)
    with open(f"tmp/{character.name}_morguefile.txt", "w") as morguefile:
        morguefile.write(f)
