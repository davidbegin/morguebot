import os
import json

import boto3


def checkout_the_weapons(event):
    print(json.dumps(event))

    for record in event["Records"]:
        body = record["body"]
        _send_chat(body)


def _send_chat(msg):
    print(f"Weapons Bot Time! {msg}")
    kinesis_arn = os.environ["CHAT_STREAM_ARN"]
    kinesis_name = os.environ["CHAT_STREAM_NAME"]

    client = boto3.client("kinesis")

    try:
        decoded_msg = json.loads(msg)
        message = decoded_msg["Message"]
    except:
        message = msg

    response = client.put_record(
        StreamName=kinesis_name,
        Data=json.dumps({"Message": f"CurseLit {message}"}),
        PartitionKey="alpha",
    )

    print(response)
