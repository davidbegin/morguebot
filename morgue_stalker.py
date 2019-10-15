import os
import json
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_saver import morgue_saver


def handler(event, handler):
    print(json.dumps(event))

    if "character" in event.keys():
        character_name = event["character"]
    elif "CHARACTER" in os.environ:
        character_name = os.environ.get("CHARACTER", None)
    else:
        character_name = "beginbot"

    character = Character(character=character_name)
    morgue_saver(character, character.morgue_file())
