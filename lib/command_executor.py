import os


from lib.character import Character
from lib.formatter import Formatter
from lib.kinesis import send_chat_to_stream
from lib.morgue_saver import morgue_saver

from lib.config import find_character_name

from lib.weapon_awards import find_the_max_damage_for_all_characters

from lib.the_real_morgue_parser import MorgueParser


def process_event(event):
    command = event["command"]
    character_name = find_character_name(event)
    character = Character(name=character_name)
    formatter = Formatter(character)
    arg1 = event.get("arg1", None)
    arg2 = event.get("arg2", None)

    if command == "!fetch":
        morgue_saver(character, character.non_saved_morgue_file())

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
    elif command == "!weapon_awards":
        find_the_max_damage_for_all_characters()
    elif command == "!search":
        for c in ["!armour", "!weapons", "!jewellery"]:
            call_command_with_arg(formatter, c, arg1)
    elif arg1:
        call_command_with_arg(formatter, command, arg1)
    else:
        call_command(formatter, command, character_name)


# ========================================================================================


def call_command(formatter, command, character_name):
    msg = formatter.construct_message(command)
    if msg:
        send_chat_to_stream(msg)
    else:
        print(f"Error building message {command} for {character_name}")


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
