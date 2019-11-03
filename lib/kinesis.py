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

    # We need to chunk the msg in chunks of 500
    response = client.put_record(
        StreamName=KINESIS_NAME, Data=json.dumps({"Message": msg}), PartitionKey="alpha"
    )

    metadata = response["ResponseMetadata"]
    status = metadata["HTTPStatusCode"]
    if status == 200:
        print(f"\033[37mMessage sent to Kinesis Stream {msg}...\033[0m")
    else:
        print(f"\033[31m{json.dumps(response)}\033m")
