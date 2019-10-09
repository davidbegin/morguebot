import json
from lib.irc_connector import connect_to_twitch
from lib.printer import Printer
from lib.runners import run_command
from lib.runners import run_status_checker

import boto3

def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False)

    if "command" in event.keys():
        command = f"!{event['command']}"
    else:
        command = "!overview"

    if "character" in event.keys():
        character = event["character"]
    else:
        character = None

    run_command(command, server, printer, character=character)

def status(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False)

    if "CHARACTER" in os.environ:
        character = os.environ["CHARACTER"]
    else:
        character = None

    run_status_checker(server, printer, character=character)

