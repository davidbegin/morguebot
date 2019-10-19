import time

import boto3

from lib.command_parser import execute_command
from lib.command_parser import process_msg
from lib.file_watcher import watch_for_changes
from lib.morgue_parser import fetch_altars


def run_bot(server, printer, character):
    while True:
        watch_for_changes()

        # I think we are blocked on waiting for a message here
        # We might want to add a timeout and retry or something
        irc_response = server.recv(2048).decode("utf-8").split()

        # How do we wan to control these prints better
        # print(irc_response)

        if len(irc_response) < 2:
            # print(irc_response)
            pass
        elif irc_response[1] == "PRIVMSG":
            process_msg(printer, irc_response, character)
        elif irc_response[0] == "PING":
            print("WE NEED TO PONG")
            server.send(bytes("PONG" + "\r\n", "utf-8"))
