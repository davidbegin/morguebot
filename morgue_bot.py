import os
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB


# This should be getting a message about S3
def handler(event, handler):
    pass
    # if "character" in event.keys():
    #     character_name = event["character"]
    # else:
    #     character_name = os.environ.get("CHARACTER", None)

    # character = Character(character=character_name)
    # skills = fetch_skills(character.morgue_file())
    # print(skills)
    # db = MorgueDB(character=character)
    # db._store_skills(skills)