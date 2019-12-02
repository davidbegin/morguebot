import os
import base64
import json

from lib.irc_connector import connect_to_twitch


def send_twitch_message(event):
    if "Records" in event:
        for record in event["Records"]:
            process_kinesis_record(record)

    # For Async
    elif "responsePayload" in event:
        send_msg(event["responsePayload"])
    else:
        send_msg(json.dumps(event))


# ========================================================================================


def process_kinesis_message(message):
    try:
        # TODO: Check Json parsibility
        msg = json.loads(message)["Message"]
        if msg:
            print(f"msg {type(msg)}: {msg}")
            if type(msg) is list:
                for m in msg:
                    print(f"m: {m}")
                    send_msg(m)
            else:
                send_msg(msg)

        else:
            print(f"Kinesis Message does not contain the 'Message' key.")
            print(f"{message}")
    except Exception as e:
        print(e)
        print(message)


def process_kinesis_record(record):
    data = record["kinesis"]["data"]
    base64_decoded = base64.b64decode(data)
    message = base64_decoded.decode("utf")

    print(json.dumps({"action": "process_kinesis_record", "message": message}))

    if "Message" in message:
        process_kinesis_message(message)
    elif "default" in message:
        send_msg(message["default"])
    else:
        send_msg(json.dumps(message))


def parse_json(item):
    try:
        return json.loads(item)
    except:
        return None


def send_msg(msg):
    server = connect_to_twitch()
    channel = os.environ.get("MORGUEBOT_CHANNEL", "beginbot")

    disable_twitch = False

    if not disable_twitch:
        if msg:
            result = server.send(
                bytes("PRIVMSG " + f"#{channel}" + " :" + msg + "\n", "utf-8")
            )
