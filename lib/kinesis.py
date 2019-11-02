import os
import json

import boto3
import botocore

KINESIS_NAME = os.environ.get("CHAT_STREAM_NAME", "twitch-chat-877759c")


def send_new_runes_msg(character, runes):
    print(f"send_new_runes_msg: {character} {runes}")
    msg = f"PraiseIt New Runes! {' - '.join(runes)} PraiseIt {character}"
    send_chat_to_stream(msg)


def send_chat_to_stream(msg):
    client = boto3.client("kinesis")

    # We need to chuunk the msg in chunks of 500

    response = client.put_record(
        StreamName=KINESIS_NAME, Data=json.dumps({"Message": msg}), PartitionKey="alpha"
    )

    print(json.dumps(response))
