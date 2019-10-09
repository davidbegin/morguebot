import json
from lib.irc_connector import connect_to_twitch
from lib.printer import Printer
from lib.runners import run_command

import boto3

def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False)
    if "command" in event.keys():
        run_command(f"!{event['command']}", server, printer)
    else:
        run_command(f"!overview", server, printer)
