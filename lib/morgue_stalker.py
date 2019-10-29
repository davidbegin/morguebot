import os
import json

import boto3

from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_saver import morgue_saver


def fetch_characters():
    if True:
        client = boto3.client("s3")
        response = client.list_objects_v2(Bucket="morgue-files-2944dfb")
        s3_objects = response["Contents"]
        morgue_keys = filter_out_morgue_keys(s3_objects)
        return sanitize_them_keys(morgue_keys)
    else:
        return [
            "Fa",
            # "12feetdeep",
            # "4zero4",
            # "AIVN",
            # "Abyss000",
            # "Airwolf",
            # "BackslashEcho",
            # "Bootz",
            # "CoolOtter",
            # "Harvey",
            # "JFunk",
            # "Jeffwins",
            # "MAWL",
            # "None",
            # "Nublar",
            # "Slevren",
            # "Splatt",
            # "Wexler",
            # "Zebrazen",
            # "ahab",
            # "artmatt",
            # "beginbot",
            # "candlehand",
            # "carwin",
            # "collin38",
            # "ddaybell",
            # "deathblob",
            # "dioxide",
            # "disciplinedyoungman",
            # "drj",
            # "emf",
            # "enop",
            # "foxor",
            # "gorper",
            # "grinrain",
            # "haverford",
            # "ilovepuk",
            # "jomj",
            # "jtro",
            # "matticus",
            # "nebn339",
            # "perc",
            # "perf",
            # "redmage",
            # "shittywizard",
            # "simcity",
        ]


def stalk(event):
    print(json.dumps(event))

    if "single_character_mode" in event:
        stalk_character(event)
    else:
        characters_to_stalk = fetch_characters()

        for character_name in characters_to_stalk:
            character = Character(name=character_name)
            morgue_saver(character, character.non_saved_morgue_file())


# ========================================================================================


def stalk_character(event):
    if "character" in event.keys():
        character_name = event["character"]
    elif "CHARACTER" in os.environ:
        character_name = os.environ.get("CHARACTER", None)
    else:
        character_name = "beginbot"

    character = Character(name=character_name)
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
