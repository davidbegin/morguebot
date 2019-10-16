import os
import json
import boto3

from lib.morgue_db import save_a_buncha_info
from lib.irc_connector import connect_to_twitch
from lib.character import Character
from lib.printer import Printer
from lib.command_parser import execute_command
from lib.morgue_parser import fetch_overview

TOPIC_ARN = os.environ["TOPIC_ARN"]


def send_morguefile_notification(character):
    # Does it matter we make multiple
    client = boto3.client("sns")

    msg = json.dumps({"default": f"New Morgue File for {character}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print(json.dumps(response))


def handler(event, handler):
    print(json.dumps(event))

    if "Records" in event:
        for record in event["Records"]:
            character = record["s3"]["object"]["key"].split("/")[0]
            # save_a_buncha_info(character)
            send_morguefile_notification(character)
    elif "s3" in event:
        character = event["s3"]["object"]["key"].split("/")[0]
        # save_a_buncha_info(character)
        send_morguefile_notification(character)
    else:
        if "character" in event.keys():
            character_name = event["character"]
        elif "CHARACTER" in os.environ:
            character_name = os.environ.get("CHARACTER", None)
        else:
            character_name = "beginbot"

        command = event["command"]
        character = Character(character=character_name)
        kinesis_arn = os.environ["CHAT_STREAM_ARN"]
        kinesis_name = os.environ["CHAT_STREAM_NAME"]

        client = boto3.client("kinesis")

        if command == "overview":
            overview = fetch_overview(character.morgue_file())
            print("=============")
            print("overview")
            print(f"{overview}")
            print("=============")

            response = client.put_record(
                StreamName=kinesis_name, Data=f"{overview}", PartitionKey="alpha"
            )
        else:
            response = client.put_record(
                StreamName=kinesis_name, Data="WE ARE CLOSE", PartitionKey="alpha"
            )

        print(response)
