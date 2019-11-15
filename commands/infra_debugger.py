import json
import boto3

TOPIC_ARN = "arn:aws:sns:us-west-2:851075464416:gods-topic-f88048a"

def sns(logger):
    client = boto3.client("sns")
    msg = json.dumps({"default": "Testing From SNS to SQS to Kinsesis!"})
    response = client.publish(
        TopicArn=TOPIC_ARN,
        Message=msg,
        MessageStructure='json',
    )

    logger.log("Testing SNS", response=response)
