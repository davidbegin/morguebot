import os
import json

import boto3
import botocore

# KINESIS_NAME = "twitch-chat-3ef1aba"

KINESIS_NAME = "error-chat-8cc7e7a"


def send_chat_to_stream(msg):
    client = boto3.client("kinesis")

    response = client.put_record(
        StreamName=KINESIS_NAME, Data=json.dumps({"Message": msg}), PartitionKey="alpha"
    )

    print(json.dumps(response))



if __name__ == "__main__":
    msg = "Hello Twitch Chat"
    send_chat_to_stream(msg)
