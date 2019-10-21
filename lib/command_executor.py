import os


from lib.morgue_db import save_a_buncha_info
from lib.character import Character
from lib.formatter import Formatter
from lib.kinesis import send_chat_to_stream
from lib.sns import send_morguefile_notification
from lib.morgue_parser import fetch_overview
from lib.morgue_saver import morgue_saver
from lib.morgue_db import fetch_and_save_weapons
from lib.morgue_stalker import fetch_characters

from lib.weapon_analyzer import MaxDamageCalculator


def execute_command(event):
    if "Records" in event or "s3" in event:
        process_s3_events(event)
    else:
        process_event(event)


# ========================================================================================


def process_event(event):
    print(event)
    command = event["command"]
    arg1 = event.get("arg1", None)

    if command == "!fetch":
        character_name = find_character_name(event)
        character = Character(character=character_name)
        morgue_saver(character, character.non_saved_morgue_file())
    elif command == "!save_info":
        print("Saving Info")
        character_name = find_character_name(event)
        character = Character(character=character_name)
        morguefile = character.s3_morgue_file()
        fetch_and_save_weapons(character_name, morguefile)
        # Or read from S3
        # with open(f"tmp/{character_name}_morguefile.txt") as morguefile:
        #     morguefile = morguefile.read()
        #     fetch_and_save_weapons(character_name, morguefile)
    elif command == "!save_morgue":
        f = character.non_saved_morgue_file()
        os.makedirs("tmp", exist_ok=True)
        with open(f"tmp/{character_name}_morguefile.txt", "w") as morguefile:
            morguefile.write(f)
    elif command == "!clean_morgue":
        clean_the_morgue()
    elif event.get("character", None) is None and command == "!weapon_awards":
        find_the_max_damage_for_all_characters()
    elif arg1:
        character_name = find_character_name(event)
        character = Character(character=character_name)
        formatter = Formatter(character)
        all_values = formatter.construct_message(command)

        filtered_values = [value for value in all_values if arg1 in value]

        if filtered_values:
            send_chat_to_stream(
                [f"Result of your search for `{arg1}`: "] + filtered_values
            )
    else:
        character_name = find_character_name(event)
        character = Character(character=character_name)
        formatter = Formatter(character)
        msg = formatter.construct_message(command)

        if msg:
            send_chat_to_stream(msg)
        else:
            print(f"Formatter return None for {command}")


# ========================================================================================


def sort_by_max_damage(elem):
    return elem["max_damage"]


def find_max_by_type(max_damages):
    # {'weapon': 'a +3 dagger of speed (weapon)', 'max_damage': 9.25, 'type': 'Short Blades'}
    types = set([weapon_info["type"] for weapon_info in max_damages])

    most_powerful_weapons = []

    for weapon_type in types:
        weapons = [
            weapon_info
            for weapon_info in max_damages
            if weapon_info["type"] == weapon_type
        ]
        weapons.sort(key=sort_by_max_damage)
        # weapons.sort(key=lambda: elem: elem["max_damage"])
        weapons[-1].update({"score": len(weapons)})
        most_powerful_weapons.append(weapons[-1])

    return most_powerful_weapons


def find_the_max_damage_for_all_characters():
    characters = fetch_characters()

    most_powerful_weapon = {"max_damage": 0}

    all_max_damages = []
    for character_name in characters:
        character = Character(character=character_name)
        max_damages = MaxDamageCalculator(character).max_damage()
        if max_damages == ["No Weapons Found!"]:
            print(
                f"\033[37mIt's ok get some weapons and come back: {character_name}\033[0m"
            )
        else:
            all_max_damages.extend(max_damages)

    max_by_type = find_max_by_type(all_max_damages)

    send_chat_to_stream(["PorscheWIN Second Annual Weapon Awards!!! PorscheWIN"])
    for the_best in max_by_type:
        send_chat_to_stream(
            [
                f"Kreygasm Winner {the_best['character']} Kreygasm - Category: {the_best['type']}",
                f"{the_best['weapon']} - {the_best['max_damage']}",
            ]
        )

    # send_chat_to_stream(
    #     [
    #         f"MOST POWERFUL WEAPON: {most_powerful_weapon['character']} - {most_powerful_weapon['weapon']} - {most_powerful_weapon['max_damage']}"
    #     ]
    # )

    # import pdb; pdb.set_trace()
    # {'weapon': 'a +3 dagger of speed (weapon)', 'max_damage': 9.25}
    # # TODO: Might want to double check on the sorting
    # contender = max_damages[-1]["max_damage"]
    # defender = most_powerful_weapon["max_damage"]
    # if contender > defender:
    #     most_powerful_weapon["max_damage"] = contender
    #     most_powerful_weapon["weapon"] = max_damages[-1]["weapon"]
    #     most_powerful_weapon["character"] = character_name

    # send_chat_to_stream(
    #     [
    #         f"MOST POWERFUL WEAPON: {most_powerful_weapon['character']} - {most_powerful_weapon['weapon']} - {most_powerful_weapon['max_damage']}"
    #     ]
    # )


# ========================================================================================


def process_s3_events(event):
    if "Records" in event:
        for record in event["Records"]:
            process_s3_event(record)
    elif "s3" in event:
        process_s3_event(event)


def process_s3_event(event):
    character = event["s3"]["object"]["key"].split("/")[0]
    save_a_buncha_info(character)
    send_morguefile_notification(character)


# ========================================================================================


def find_character_name(event):
    if "character" in event.keys():
        character_name = event["character"]
    elif "CHARACTER" in os.environ:
        character_name = os.environ.get("CHARACTER", None)
    else:
        character_name = "beginbot"

    return character_name
