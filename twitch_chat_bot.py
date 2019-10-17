import time
import base64
import json
import os

from lib.command_parser import execute_command
from lib.printer import Printer
from lib.irc_connector import connect_to_twitch
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB


def parse_json(item):
    try:
        return json.loads(item)
    except:
        return None


def handler(event, context):
    print(json.dumps(event))

    character = Character(character=None)
    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False, character=character)

# {"Records": [{"kinesis": {"kinesisSchemaVersion": "1.0", "partitionKey": "alpha", "sequenceNumber": "49600394564044098688918732221591359812065286560470269954", "data": "eyJNZXNzYWdlIjogbnVsbH0=", "approximateArrivalTimestamp": 1571196816.458}, "eventSource": "aws:kinesis", "eventVersion": "1.0", "eventID": "shardId-000000000000:49600394564044098688918732221591359812065286560470269954", "eventName": "aws:kinesis:record", "invokeIdentityArn": "arn:aws:iam::851075464416:role/twitch-chat-bot-role-e769d19", "awsRegion": "us-west-2", "eventSourceARN": "arn:aws:kinesis:us-west-2:851075464416:stream/twitch-chat-877759c"}]}

    for record in event["Records"]:
        kinesis_record = record["kinesis"]

        if "data" in kinesis_record:
            data = kinesis_record["data"]
            base64_decoded = base64.b64decode(data)
            message = base64_decoded.decode("utf")
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            print(message)
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

            if "Message" in message:
                try:
                    msg = json.loads(message)["Message"]
                    if msg:
                        printer.send_msg(msg)
                    else:
                        print("YO YOUR MESSAGE IS NONE")
                except:
                    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    # This is a morgue file
                    print(message)
                    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    # print(message)
                    # printer.send_msg("HERE I AM ALL SAD")
                    # printer.send_msg(message)
            elif "default" in message:
                printer.send_msg(message["default"])
            else:
                printer.send_msg(json.dumps(message))
        elif "default" in kinesis:
            msq = json.loads(kinesis_record["default"])["Message"]
            printer.send_msg(msg)
        else:
            print(kinesis_record)
