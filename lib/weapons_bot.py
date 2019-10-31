import os
import json

import boto3


def check_for_unrands(gossiper):
    new_unrands = [
        weapon for weapon in gossiper.new_weapons() if PawnStar(weapon).is_unrand()
    ]
    if new_unrands:
        print(f"PRINT WE FOUND NEW UNRAND {new_unrands}")
        for unrand in new_unrands:
            send_unrand_notification(gossiper.character, unrand)
    else:
        print(f"\033[33mSorry {gossiper.character} no new unrand\033[0m")


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
