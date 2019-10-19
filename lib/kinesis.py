import os
import json

import boto3
import botocore

# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.core import patch_all

# patch_all()

KINESIS_NAME = os.environ.get("CHAT_STREAM_NAME", "twitch-chat-877759c")


def send_chat_to_stream(msg):
    client = boto3.client("kinesis")

    response = client.put_record(
        StreamName=KINESIS_NAME, Data=json.dumps({"Message": msg}), PartitionKey="alpha"
    )

    print(json.dumps(response))

