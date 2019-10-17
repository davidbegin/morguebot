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

TOPIC_ARN = os.environ["TOPIC_ARN"]
KINESIS_NAME = os.environ["CHAT_STREAM_NAME"]


def send_morguefile_notification(character):
    # Does it matter we make multiple
    client = boto3.client("sns")

    msg = json.dumps({"default": f"New Morgue File for {character}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print(json.dumps(response))


def handler(event, handler):
    print(json.dumps(event))

    # RESPOND TO S3
    if "Records" in event:
        for record in event["Records"]:
            character = record["s3"]["object"]["key"].split("/")[0]
            # save_a_buncha_info(character)
            send_morguefile_notification(character)
    # RESPOND TO S3
    elif "s3" in event:
        character = event["s3"]["object"]["key"].split("/")[0]
        # save_a_buncha_info(character)
        send_morguefile_notification(character)

    # This is direct invocation
    else:
        if "character" in event.keys():
            character_name = event["character"]
        elif "CHARACTER" in os.environ:
            character_name = os.environ.get("CHARACTER", None)
        else:
            character_name = "beginbot"

        command = event["command"]
        character = Character(character=character_name)

        client = boto3.client("kinesis")

        formatter = Formatter(character)

        msg = formatter.construct_message(command)

        response = client.put_record(
            StreamName=KINESIS_NAME,
            Data=json.dumps({"Message": msg}),
            PartitionKey="alpha",
        )

        print(response)
