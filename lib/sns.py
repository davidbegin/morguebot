import os
import json
import boto3


# In a Lambda Pulumi has the environment variables
# Locally we want to run code, touches that AWS infrastructure
# Pulumi outputs could be marked to be turned into environment variables???

# Everytime you create a Lambda and add an environment variable, then itss automatically exposed in some easy way
# to be used locally.
# .env file???
TOPIC_ARN = "arn:aws:sns:us-west-2:851075464416:gods-queue-topic-94691e5"


TOPIC_ARN = os.environ.get(
    "TOPIC_ARN", "arn:aws:sns:us-west-2:851075464416:gods-queue-topic-94691e5"
)


def send_morguefile_notification(character):
    client = boto3.client("sns")
    msg = json.dumps({"default": f"New Morgue File for {character}"})
    response = client.publish(TopicArn=TOPIC_ARN, Message=msg, MessageStructure="json")
    print(json.dumps(response))
