import os
import json
import boto3


# This should be getting a message about S3
def handler(event, handler):
    print(json.dumps(event))
    topic_arn = os.environ["TOPIC_ARN"]
    client = boto3.client("sns")

    if "Records" in event:
        print("WE HAVE RECORDS!!!")

        for record in event["Records"]:
            character = record["s3"]["object"]["key"].split("/")[0]
            print(json.dumps({"character": character}))

            # Whatever key here, twitch-chat-bot-needs
            msg = json.dumps({"default": f"New Morgue File for {character}", "message": "nice"})
            response = client.publish(
                TopicArn=topic_arn, Message=msg, MessageStructure="json"
            )
            print(f"SNS Response: {response}")
    else:
        print("WE HAVE 1 RECORD!!!")

        character = event["s3"]["object"]["key"].split("/")[0]
        print(json.dumps({"character": character}))
        msg = json.dumps({"default": f"New Morgue File for {character}"})
        response = client.publish(
            TopicArn=topic_arn, Message=msg, MessageStructure="json"
        )
        print(response)
