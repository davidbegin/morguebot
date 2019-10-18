import os
import json
import boto3
import botocore

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all



TOPIC_ARN = os.environ.get(
    "TOPIC_ARN", "arn:aws:sns:us-west-2:851075464416:gods-queue-topic-94691e5"
)


def send_morguefile_notification(character):
    client = boto3.client("sns")

    msg = json.dumps({"default": f"New Morgue File for {character}"})

    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")

    print(json.dumps(response))

