import json

from lib.kinesis import send_chat_to_stream


def monitor_the_gods(event):
    for record in event["Records"]:
        body = record["body"]
        msg = json.loads(body)["Message"]
        # For the future, we are going to modify this message
        send_chat_to_stream(msg)
