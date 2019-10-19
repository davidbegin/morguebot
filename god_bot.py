import json
import os

import boto3

from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()


def send_chat(msg):
    kinesis_arn = os.environ["CHAT_STREAM_ARN"]
    kinesis_name = os.environ["CHAT_STREAM_NAME"]

    client = boto3.client("kinesis")
    response = client.put_record(
        StreamName=kinesis_name, Data=msg, PartitionKey="alpha"
    )

    print(response)


def handler(event, handler):
    print(json.dumps(event))

    for record in event["Records"]:
        body = record["body"]

        # For the future, we are going to modify this message
        send_chat(body)
