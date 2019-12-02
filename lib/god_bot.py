import json

from lib.kinesis import send_chat_to_stream


def parse_json(body):
    decoded_body = json.loads(body)
    msg = decoded_body["Message"]

    if isinstance(msg, str):
        parsed_msg = json.loads(msg)["responsePayload"]

        error_type = parsed_msg["errorType"]
        stack_trace = [str(stack) for stack in parsed_msg["stackTrace"][0]]

        return f"Error: {error_type}: {' '.join(stack_trace)}"
    else:
        print("msg is not a String??")
        return msg


def monitor_the_gods(event):
    for record in event["Records"]:
        msg = parse_json(record["body"])
        send_chat_to_stream(msg)
