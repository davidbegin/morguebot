import os
from lib.command_parser import execute_command
from lib.printer import Printer
from lib.irc_connector import connect_to_twitch
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB


def handler(event, handler):
    print("I'm twitch_chat_bot!")

    if "command" in event.keys():
        command = f"!{event['command']}"
    else:
        command = "!overview"

    if "character" in event.keys():
        character = event["character"]
    else:
        character = None

    character = Character(character=character)

    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False, character=character)
    execute_command(printer, command, character)


handler({}, {})
