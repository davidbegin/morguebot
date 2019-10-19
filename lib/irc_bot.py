import json
import time

import boto3

from lib.file_watcher import watch_for_changes
from lib.morgue_parser import fetch_altars


def run_bot(server, character):
    while True:
        # watch_for_changes()

        # I think we are blocked on waiting for a message here
        # We might want to add a timeout and retry or something
        irc_response = server.recv(2048).decode("utf-8").split()

        # How do we wan to control these prints better
        # print(irc_response)

        if len(irc_response) < 2:
            # print(irc_response)
            pass
        elif irc_response[1] == "PRIVMSG":
            _process_msg(irc_response, character)
        elif irc_response[0] == "PING":
            print("WE NEED TO PONG")
            server.send(bytes("PONG" + "\r\n", "utf-8"))


# ========================================================================================


def process_msg(irc_response, character):
    user, msg = _parse_user_and_msg(irc_response)

    if _is_command_msg(msg):
        split_command = msg.split()
        command = split_command[0]

        if len(split_command) > 1:
            character_name = split_command[1]
        else:
            character_name = character.character

        invoke_morgue_bot(character_name, command)
    else:
        print(f"\033[37;1m{user}:\033[0m {msg}")


def invoke_morgue_bot(character, command):
    print("invoke_morgue_bot")
    client = boto3.client("lambda")

    payload = {"character": character, "command": command}
    client.invoke(FunctionName="morgue-bot-2fc463f", Payload=json.dumps(payload))


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
