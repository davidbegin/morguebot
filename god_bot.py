import json
import os
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB

import boto3


def send_chat(msg):
    kinesis_arn = "arn:aws:kinesis:us-west-2:851075464416:stream/twitch-chat-877759c"
    kinesis_name = "twitch-chat-877759c"

    client = boto3.client("kinesis")
    response = client.put_record(
        StreamName=kinesis_name, Data=msg, PartitionKey="alpha"
    )

    print(response)


def handler(event, handler):
    print(json.dumps(event))

    for record in event["Records"]:
        body = record["body"]
        send_chat(body)
