import os
import json
import boto3


# In a Lambda Pulumi has the environment variables
# Locally we want to run code, touches that AWS infrastructure
# Pulumi outputs could be marked to be turned into environment variables???

# Everytime you create a Lambda and add an environment variable, then itss automatically exposed in some easy way
# to be used locally.
# .env file???

TOPIC_ARN = os.environ.get(
    "TOPIC_ARN", "arn:aws:sns:us-west-2:851075464416:gods-queue-topic-94691e5"
)

WEAPONS_ARN = os.environ.get(
    "WEAPONS_ARN", "arn:aws:sns:us-west-2:851075464416:weapons-topic-f819b3f"
)


def send_unrand_notification(character, unrand):
    client = boto3.client("sns")
    msg = json.dumps(
        {"default": f"CurseLit New Unrand {unrand} {character.overview()}"}
    )
    response = client.publish(
        TopicArn=WEAPONS_ARN, Message=msg, MessageStructure="json"
    )
    print(json.dumps(response))


def send_morguefile_notification(character):
    client = boto3.client("sns")
    msg = json.dumps({"default": f"New Morgue File for {character.overview()}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print(json.dumps(response))
