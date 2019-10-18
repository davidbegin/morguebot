import os
import json
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_saver import morgue_saver

import boto3
import botocore
import requests

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def handler(event, handler):
    print(json.dumps(event))

    if "character" in event.keys():
        character_name = event["character"]
    elif "CHARACTER" in os.environ:
        character_name = os.environ.get("CHARACTER", None)
    else:
        character_name = "beginbot"

    character = Character(character=character_name)
    morgue_saver(character, character.non_saved_morgue_file())
