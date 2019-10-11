#!/usr/bin/python

import time

from optparse import OptionParser

from lib.command_parser import execute_command
from lib.irc_connector import connect_to_twitch
from lib.printer import Printer
from lib.runners import run_bot
from lib.morgue_finder import fetch_morgue_file
from lib.morgue_parser import fetch_altars

from lib.character import Character
from lib.status_checkers import check_for_new_gods
from lib.status_checkers import validate_seed


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

    # Run in Different Modes
    parser.add_option(
        "-e", "--exec-cmd", action="store", type="string", dest="exec_command"
    )
    parser.add_option(
        "-s", "--status-checker", action="store_true", dest="status_checker"
    )

    # Printer Options
    parser.add_option(
        "-d", "--disable-twitch", action="store_true", dest="disable_twitch"
    )

    (options, args) = parser.parse_args()

    server = connect_to_twitch()
    printer = Printer(
        server, disable_twitch=options.disable_twitch, character=options.character
    )

    character = Character(
        morgue_filepath=options.morgue_filepath,
        morgue_url=options.morgue_url,
        character=options.character,
        local_mode=options.local_mode,
    )

    if options.exec_command:
        execute_command(printer, f"!{options.exec_command}", character.morgue_file())
    elif options.status_checker:
        while True:
            validate_seed(character)
            check_for_new_gods(character, printer)
            time.sleep(3)
    else:
        run_bot(
            server,
            printer,
            morgue_filepath=options.morgue_filepath,
            morgue_url=options.morgue_url,
            character=options.character,
            local_mode=options.local_mode,
        )


if __name__ == "__main__":
    exit(main())
