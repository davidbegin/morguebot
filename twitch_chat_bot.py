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
                    if "default" in message:
                        printer.send_msg(message["default"])
                    else:
                        printer.send_msg(message)

                    # if parse_json(message):
                    #     m = json.loads(message)
                    #     import pdb; pdb.set_trace()
                    #     # print(m)
                    #     printer.send_msg(m["Message"])
                    # else:
                    #     print("NOT PARSEABLE BY JSON")
                    #     print(message)

                elif "default" in kinesis:
                    msq = json.loads(kinesis_record["default"])["Message"]
                    printer.send_msg(msg)
                else:
                    pass
                    # print(kinesis_record)
                time.sleep(1)
            else:
                pass
                # print(record)


# handler({}, {})
