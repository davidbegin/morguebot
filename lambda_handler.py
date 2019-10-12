import os
import json
from lib.irc_connector import connect_to_twitch
from lib.printer import Printer
from lib.command_parser import execute_command
from lib.character import Character
from lib.status_checkers import check_for_new_gods

import boto3


def save_morgue(event, context):
    print("SAVE tHE MORGUE!!!!!!!!!")
    # print("Received event: " + json.dumps(event, indent=2))

    server = connect_to_twitch()

    if "command" in event.keys():
        command = f"!{event['command']}"
    else:
        command = "!overview"

    if "character" in event.keys():
        character = event["character"]
    else:
        character = None

    character = Character(character=character)
    print(f"character: {character.character}")
    character.morgue_file()


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    server = connect_to_twitch()

    if "command" in event.keys():
        command = f"!{event['command']}"
    else:
        command = "!overview"

    if "character" in event.keys():
        character = event["character"]
    else:
        character = None

    printer = Printer(server, disable_twitch=False, character=character)
    character = Character(character=character)
    execute_command(printer, command, character.morgue_file())


def overview(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    server = connect_to_twitch()

    if "CHARACTER" in os.environ:
        character = os.environ["CHARACTER"]
    else:
        character = None
    printer = Printer(server, disable_twitch=False, character=character)
    character = Character(character=character)
    execute_command(printer, "!overview", character.morgue_file())


def status(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    server = connect_to_twitch()

    if "CHARACTER" in os.environ:
        character = os.environ["CHARACTER"]
    else:
        character = None

    print(f"character: {character}")

    printer = Printer(server, disable_twitch=False, character=character)
    character = Character(character=character)
    check_for_new_gods(character, printer)
