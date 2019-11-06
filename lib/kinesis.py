import os
import textwrap
import json

import boto3
import botocore
from lib.response_printer import print_response

KINESIS_NAME = os.environ.get("CHAT_STREAM_NAME", "twitch-chat-877759c")

client = boto3.client("kinesis")


def send_new_runes_msg(character, runes):
    print(f"send_new_runes_msg: {character} {runes}")
    msg = f"PraiseIt New Runes! {' - '.join(runes)} PraiseIt {character}"
    send_chat_to_stream(msg)


def send_chat_to_stream(msg):
    if type(msg) is list:
        nested_msg = [textwrap.wrap(sub_msg, 500) for sub_msg in msg]
        # Flattening List
        msg = [item for sublist in nested_msg for item in sublist]

    put_kinesis_record(msg)


def put_kinesis_record(msg):
    response = client.put_record(
        StreamName=KINESIS_NAME, Data=json.dumps({"Message": msg}), PartitionKey="alpha"
    )

    print_response(response, msg, "Message sent to Kinesis Stream")
