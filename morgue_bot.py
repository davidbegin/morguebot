import os
import json
import boto3
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB


# This should be getting a message about S3
def handler(event, handler):
    print("I'm morgue_bot!")

    # print(f"event: {event}")

    # print(json.dumps(event, indent=2))

    for record in event["Records"]:
        character = record["s3"]["object"]["key"].split("/")[0]
        # [character = print("Keys: {record.keys()}")

        topic_arn = "arn:aws:sns:us-west-2:851075464416:god-queue-topic-a3644eb"
        client = boto3.client("sns")

        msg = json.dumps({"default": f"New Morgue File for {character}"})

        response = client.publish(
            TopicArn=topic_arn, Message=msg, MessageStructure="json"
        )
