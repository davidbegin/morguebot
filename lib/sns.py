import os
import json
import boto3

from lib.response_printer import print_response


# In a Lambda Pulumi has the environment variables
# Locally we want to run code, touches that AWS infrastructure
# Pulumi outputs could be marked to be turned into environment variables???

# Everytime you create a Lambda and add an environment variable, then itss automatically exposed in some easy way
# to be used locally.
# .env file???

TOPIC_ARN = os.environ.get(
    "TOPIC_ARN", "arn:aws:sns:us-west-2:851075464416:gods-topic-f88048a"
)

WEAPONS_ARN = os.environ.get(
    "WEAPONS_ARN", "arn:aws:sns:us-west-2:851075464416:weapons-topic-f819b3f"
)


def send_new_weapons_notification(character, weapons):
    client = boto3.client("sns")
    msg = json.dumps(
        {"default": json.dumps({"character": f"{character.name}", "weapons": weapons})}
    )
    response = client.publish(
        TopicArn=WEAPONS_ARN, Message=msg, MessageStructure="json"
    )
    print_response(response, msg, "Message sent to SNS Topic")


def send_new_runes_notification(character, runes):
    client = boto3.client("sns")
    msg = json.dumps(
        {"default": json.dumps({"character": f"{character.name}", "runes": runes})}
    )
    response = client.publish(
        TopicArn=WEAPONS_ARN, Message=msg, MessageStructure="json"
    )
    print_response(response, msg, "Message sent to SNS Topic")


def send_morguefile_notification(character):
    client = boto3.client("sns")
    msg = json.dumps({"default": f"New Morgue File for {character.overview()}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print_response(response, msg, "Message sent to SNS Topic")
