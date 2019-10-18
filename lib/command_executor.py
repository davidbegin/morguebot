import os
import json
import boto3

from lib.morgue_db import save_a_buncha_info
from lib.irc_connector import connect_to_twitch
from lib.character import Character
from lib.printer import Printer
from lib.command_parser import execute_command
from lib.morgue_parser import fetch_overview
from lib.formatter import Formatter

TOPIC_ARN = os.environ.get(
    "TOPIC_ARN", "arn:aws:sns:us-west-2:851075464416:gods-queue-topic-94691e5"
)
KINESIS_NAME = os.environ.get("CHAT_STREAM_NAME", "twitch-chat-877759c")


def execute_command(event):
    if "Records" in event or "s3" in event:
        process_s3_events(event)
    else:
        process_event(event)


# ========================================================================================


def send_morguefile_notification(character):
    client = boto3.client("sns")
    msg = json.dumps({"default": f"New Morgue File for {character}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print(json.dumps(response))


def send_chat_to_stream(msg):
    client = boto3.client("kinesis")
    response = client.put_record(
        StreamName=KINESIS_NAME, Data=json.dumps({"Message": msg}), PartitionKey="alpha"
    )
    print(json.dumps(response))


def process_s3_events(event):
    if "Records" in event:
        for record in event["Records"]:
            process_s3_event(record)
    elif "s3" in event:
        process_s3_event(event)


def process_s3_event():
    character = event["s3"]["object"]["key"].split("/")[0]
    # save_a_buncha_info(character)
    send_morguefile_notification(character)


def find_character_name(event):
    if "character" in event.keys():
        character_name = event["character"]
    elif "CHARACTER" in os.environ:
        character_name = os.environ.get("CHARACTER", None)
    else:
        character_name = "beginbot"

    return character_name


def process_event(event):
    character_name = find_character_name(event)
    command = event["command"]
    character = Character(character=character_name)

    formatter = Formatter(character)
    msg = formatter.construct_message(command)

    if msg:
        send_chat_to_stream(msg)
    else:
        print(f"Formatter return None for {command}")
