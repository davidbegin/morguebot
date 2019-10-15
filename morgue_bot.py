import os
import json
import boto3

from lib.morgue_db import save_a_buncha_info

TOPIC_ARN = os.environ["TOPIC_ARN"]


def download_morguefile(bucket, key):
    client = boto3.client("s3")
    response = client.get_object(Bucket=bucket, Key=key)
    morguefile = response["Body"].read()

    print(morguefile)


def send_morguefile_notification(character):
    # Does it matter we make multiple
    client = boto3.client("sns")

    msg = json.dumps({"default": f"New Morgue File for {character}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print(json.dumps(response))


def handler(event, handler):
    print(json.dumps(event))

    if "Records" in event:
        for record in event["Records"]:
            character = record["s3"]["object"]["key"].split("/")[0]

            save_a_buncha_info(character)
            # parse_morguefile(record["s3"])
            send_morguefile_notification(character)
    else:
        character = event["s3"]["object"]["key"].split("/")[0]
        save_a_buncha_info(character)
        # parse_morguefile(record["s3"])
        send_morguefile_notification(character)
