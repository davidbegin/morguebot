# import os
# import json
# import boto3

from lib.kinesis import send_chat_to_stream


def monitor_the_gods(event):
    for record in event["Records"]:
        body = record["body"]
        # For the future, we are going to modify this message
        send_chat_to_stream(body)


# def _send_chat(msg):
#     kinesis_arn = os.environ["CHAT_STREAM_ARN"]
#     kinesis_name = os.environ["CHAT_STREAM_NAME"]

#     client = boto3.client("kinesis")
#     response = client.put_record(
#         StreamName=kinesis_name, Data=msg, PartitionKey="alpha"
#     )

#     print(response)
