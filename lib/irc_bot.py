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

        if irc_response[1] == "PRIVMSG":
            user, msg = _parse_user_and_msg(irc_response)
            if _is_command_msg(msg):
                morgue_event = TwitchChatParser(msg).parse()
                EventCoordinator(morgue_event).coordinate()
            else:
                print(f"\033[37;1m{user}:\033[0m {msg}")
        elif irc_response[0] == "PING":
            server.send(bytes("PONG" + "\r\n", "utf-8"))


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
