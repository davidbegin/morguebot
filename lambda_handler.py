import os
import json


import boto3
import botocore
import requests

if os.environ.get("AWS_LAMBDA_FUNCTION_NAME", None):
    from aws_xray_sdk.core import xray_recorder
    from aws_xray_sdk.core import patch_all

    patch_all()

from lib.twitch_chat_bot import send_twitch_message
from lib.command_executor import execute_command


def twitch_chat_bot(event, context):
    print(json.dumps(event))
    send_twitch_message(event)


def morgue_bot(event, handler):
    print(json.dumps(event))
    execute_command(event)


def god_bot(event, context):
    print(json.dumps(event))

    for record in event["Records"]:
        body = record["body"]
        # For the future, we are going to modify this message
        _send_chat(body)


def xl_bot(event, handler):
    print("I'm xl_bot!")


def _send_chat(msg):
    kinesis_arn = os.environ["CHAT_STREAM_ARN"]
    kinesis_name = os.environ["CHAT_STREAM_NAME"]

    client = boto3.client("kinesis")
    response = client.put_record(
        StreamName=kinesis_name, Data=msg, PartitionKey="alpha"
    )

    print(response)
