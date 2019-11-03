import json
import time

import boto3

from lib.file_watcher import watch_for_changes
from lib.morgue_parser import fetch_altars
from lib.twitch_chat_parser import TwitchChatParser
from lib.event_coordinator import EventCoordinator
from lib.command_executor import process_event


def run_bot(server, character):
    while True:
        # watch_for_changes()

        irc_response = server.recv(2048).decode("utf-8").split()
        # event = {"character": None, "command" : "!h?", "args": []}
        # process_event(event)
        # return

        if len(irc_response) < 2:
            pass
        elif irc_response[1] == "PRIVMSG":
            _process_msg(irc_response, character)
        elif irc_response[0] == "PING":
            server.send(bytes("PONG" + "\r\n", "utf-8"))


# ========================================================================================


def _process_msg(irc_response, character):
    user, msg = _parse_user_and_msg(irc_response)
    if _is_command_msg(msg):
        morgue_event = TwitchChatParser(msg).parse()
        EventCoordinator(morgue_event).coordinate()
    else:
        print(f"\033[37;1m{user}:\033[0m {msg}")


# TODO: refactor this sillyness
def _parse_user_and_msg(irc_response):
    user_info, _, _, *raw_msg = irc_response
    raw_first_word, *raw_rest_of_the_message = raw_msg
    first_word = raw_first_word[1:]
    rest_of_the_message = " ".join(raw_rest_of_the_message)
    user = user_info.split("!")[0][1:]
    msg = f"{first_word} {rest_of_the_message}"
    return user, msg


def _is_command_msg(msg):
    return msg[0] == "!" and msg[1] != "!"


# ========================================================================================

# def invoke_morgue_stalker(character):
#     payload = {
#         "character": character,
#         "command": "!fetch",
#         "single_character_mode": True,
#     }
#     client = boto3.client("lambda")
#     client.invoke(FunctionName="morgue-stalker-341e60e", Payload=json.dumps(payload))
#
# def _old_process_msg(irc_response, character):
#     user, msg = _parse_user_and_msg(irc_response)
#     character_name = None
#     arguments = None

#     if _is_command_msg(msg):
#         split_command = msg.split()
#         command = split_command[0]

#         if command == "!h?":
#             character_name = None
#             # Can we return early here??
#             return invoke_dungeon_gossiper(character_name, command)
#         elif len(split_command) == 1:
#             print(f"\033[31mWe are not going to execute: command: {command}\033[0m")
#         elif len(split_command) == 2:
#             arguments = None
#             character_name = split_command[1]
#         elif len(split_command) > 2:
#             arguments = split_command[2:]
#             character_name = split_command[1]

#         if command == "!fetch":
#             invoke_morgue_stalker(character_name)
#         else:
#             invoke_dungeon_gossiper(character_name, command, arguments)
#     else:
#         print(f"\033[37;1m{user}:\033[0m {msg}")


# def invoke_dungeon_gossiper(character, command, arguments=None):
#     print(
#         f"\033[33mInvoking Morgue Bot\033[0m \033[037;1mcharacter:\033[0m \033[36m{character}\033[0m \033[37;1mcommand:\033[0m \033[36m{command}\033[0m"
#     )
#     client = boto3.client("lambda")

#     if arguments:
#         if len(arguments) > 1:
#             payload = {
#                 "character": character,
#                 "command": command,
#                 "arg1": arguments[0],
#                 "arg2": arguments[1],
#             }
#         elif len(arguments) == 1:
#             payload = {"character": character, "command": command, "arg1": arguments[0]}
#         else:
#             payload = {"character": character, "command": command, "arg1": arguments[1]}
#     else:
#         payload = {"character": character, "command": command}

#     # We need to pull this in from Pulumi
#     client.invoke(FunctionName="dungeon_gossiper-67e2768", Payload=json.dumps(payload))
