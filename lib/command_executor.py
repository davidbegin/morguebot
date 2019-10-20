import os

from lib.morgue_db import save_a_buncha_info
from lib.character import Character
from lib.formatter import Formatter
from lib.kinesis import send_chat_to_stream
from lib.sns import send_morguefile_notification
from lib.morgue_parser import fetch_overview
from lib.morgue_saver import morgue_saver
from lib.morgue_db import fetch_and_save_weapons


def execute_command(event):
    if "Records" in event or "s3" in event:
        process_s3_events(event)
    else:
        process_event(event)


# ========================================================================================


def process_event(event):
    character_name = find_character_name(event)
    command = event["command"]
    character = Character(character=character_name)

    if command == "!fetch":

        morgue_saver(character, character.non_saved_morgue_file())

    elif command == "!save_info":
        print("Saving Info")
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
    else:
        formatter = Formatter(character)
        msg = formatter.construct_message(command)

        if msg:
            send_chat_to_stream(msg)
        else:
            print(f"Formatter return None for {command}")


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
