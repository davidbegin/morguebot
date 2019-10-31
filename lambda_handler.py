import os
import json

import boto3
import botocore
import requests

if os.environ.get("AWS_LAMBDA_FUNCTION_NAME", None):
    from aws_xray_sdk.core import xray_recorder
    from aws_xray_sdk.core import patch_all

    patch_all()

from lib.command_executor import process_event
from lib.execute_s3_command import process_s3_events
from lib.god_bot import monitor_the_gods
from lib.weapons_bot import checkout_the_weapons
from lib.morgue_stalker import stalk
from lib.twitch_chat_bot import send_twitch_message

# from lib.dungeon_gossiper import process_dynamodb_records
from lib.dungeon_gossiper import DungeonGossiper


def morgue_stalker(event, handler):
    print(json.dumps(event))
    stalk(event)


def twitch_chat_bot(event, context):
    print(json.dumps(event))
    send_twitch_message(event)


# MorgueFileProcessor
def morgue_bot(event, handler):
    print(json.dumps(event))
    if "Records" in event or "s3" in event:
        process_s3_events(event)
    else:
        process_event(event)


def god_bot(event, context):
    print(json.dumps(event))
    monitor_the_gods(event)


def xl_bot(event, handler):
    print(json.dumps(event))
    monitor_the_gods(event)


def dungeon_gossiper(event, context):
    print(json.dumps(event))
    for record in event["Records"]:
        gossiper = DungeonGossiper(record)
        # check_for_unrands(gossiper)
        if gossiper.new_weapons():
            print(f"We got some new weapons: {gossiper.weapons()}")
            send_new_weapon_notification(gossiper.character, gossiper.new_weapons())
        if gossiper.new_runes():
            print(f"We Got new runes {gossiper.new_runes()}")
            send_new_runes_notification(gossiper.character, gossiper.new_runes())


def weapons_bot(event, context):
    print(json.dumps(event))
    checkout_the_weapons(event)
