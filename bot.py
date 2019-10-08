#!/usr/bin/python

from optparse import OptionParser

from lib.irc_connector import connect_to_twitch
from lib.printer import Printer
from lib.runners import run_bot
from lib.runners import run_command


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

    # Run in Bot Mode or single command
    parser.add_option(
        "-e", "--exec-cmd", action="store", type="string", dest="exec_command"
    )

    # Printer Options
    parser.add_option(
        "-d", "--disable-twitch", action="store_true", dest="disable_twitch"
    )

    (options, args) = parser.parse_args()

    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=options.disable_twitch)

    if options.exec_command:
        run_command(
            f"!{options.exec_command}",
            server,
            printer,
            morgue_filepath=options.morgue_filepath,
            morgue_url=options.morgue_url,
            character=options.character,
            local_mode=options.local_mode,
        )
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
