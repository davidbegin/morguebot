#!/usr/bin/python

import time

from optparse import OptionParser

from lib.command_executor import process_event
from lib.irc_connector import connect_to_twitch
from lib.irc_bot import run_bot

from lib.character import Character
from lib.kinesis import send_chat_to_stream


def main():
    parser = OptionParser()

    # Where to find the Morgue File
    parser.add_option("-c", "--char", action="store", type="string", dest="character")
    parser.add_option("-l", "--local", action="store_true", dest="local_mode")
    parser.add_option(
        "-m", "--morgue-file", action="store", type="string", dest="morgue_filepath"
    )
    parser.add_option(
        "-u", "--morgue-url", action="store", type="string", dest="morgue_url"
    )

    parser.add_option("-s", "--search", action="store", type="string", dest="search")
    parser.add_option(
        "-b", "--level-barrier", action="store", type="string", dest="level_barrier"
    )

    # Run in Different Modes
    parser.add_option(
        "-e", "--exec-cmd", action="store", type="string", dest="exec_command"
    )

    # Whether to have the bot post back to Twitch
    parser.add_option(
        "-d", "--disable-twitch", action="store_true", dest="disable_twitch"
    )

    (options, args) = parser.parse_args()

    server = connect_to_twitch()

    character = Character(
        morgue_filepath=options.morgue_filepath,
        morgue_url=options.morgue_url,
        name=options.character,
        local_mode=options.local_mode,
    )

    # Create a MorgueEvent
    # LOCAL
    # CommandLineParser.from_options(options)

    # MorgueEvent(command=, character= args=f])
    if options.exec_command:
        # send_chat_to_stream(f"pastaThat Character: {character.name} pastaThat")
        process_event(
            {
                "character": options.character,
                "command": f"!{options.exec_command}",
                "level_barrier": options.level_barrier,
                # "arg1": options.arg1,
                # "arg2": options.arg2,
            }
        )
    else:
        # TWITCH CHAT
        run_bot(server, character=character)


if __name__ == "__main__":
    exit(main())
