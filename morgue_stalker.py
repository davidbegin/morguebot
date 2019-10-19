import os
import json
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_saver import morgue_saver

import boto3
import botocore
import requests

if os.environ.get("AWS_LAMBDA_FUNCTION_NAME", None):
    from aws_xray_sdk.core import xray_recorder
    from aws_xray_sdk.core import patch_all

    patch_all()


def stalk_character(event):
    if "character" in event.keys():
        character_name = event["character"]
    elif "CHARACTER" in os.environ:
        character_name = os.environ.get("CHARACTER", None)
    else:
        character_name = "beginbot"

    character = Character(character=character_name)
    morgue_saver(character, character.non_saved_morgue_file())


def chandler(event, handler):
    print(json.dumps(event))
    # stalk_character(event)

    client = boto3.client("s3")
    response = client.list_objects_v2(
        Bucket="morgue-files-2944dfb",
    )
    s3_objects = response["Contents"]

    morgue_keys = filter_out_morgue_keys(s3_objects)
    characters_to_stalk = sanitize_them_keys(morgue_keys)
    for character_name in characters_to_stalk:
        character = Character(character=character_name)
        morgue_saver(character, character.non_saved_morgue_file())


def sanitize_them_keys(morgue_keys):
    return [
        morgue_key.split("/")[0]
        for morgue_key in morgue_keys
        if (len(morgue_key.split("/")) == 2)
    ]


def filter_out_morgue_keys(s3_objects):
    return [
        s3_object["Key"]
        for s3_object in s3_objects
        if s3_object["Key"].endswith("morguefile.txt")
    ]


# chandler({}, {})
