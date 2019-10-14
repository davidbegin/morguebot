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


def handler(event, context):
    print(json.dumps(event))

    character = Character(character=None)
    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False, character=character)

    if "Records" not in event:
        printer.send_msg("Testing")
    else:
        for record in event["Records"]:

            if "kinesis" in record:

                kinesis_record = record["kinesis"]

                if "data" in kinesis_record:
                    data = record["kinesis"]["data"]
                    base64_decoded = base64.b64decode(data)
                    message = base64_decoded.decode("utf")

                    m = json.loads(message)
                    print(m)
                    printer.send_msg(m["Message"])

                elif "message":
                    msq = json.loads(kinesis_record["message"])["Message"]
                    printer.send_msg(msg)
                else:
                    print(kinesis_record)
                time.sleep(1)
            else:
                print(record)


# handler({}, {})
