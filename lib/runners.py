from lib.command_parser import execute_command
from lib.command_parser import process_msg
from lib.morgue_finder import fetch_morgue_file
from lib.status_checkers import check_for_new_gods
from lib.file_watcher import watch_for_changes


def run_command(
    command,
    server,
    printer,
    morgue_filepath=None,
    morgue_url=None,
    character=None,
    local_mode=False,
):

    # import requests
    # x = requests.get("http://crawl.akrasiac.org/scoring/all-players.html")
    # # x = requests.get("http://crawl.akrasiac.org:8080/#lobby")
    # # x = requests.get("http://crawl.akrasiac.org/scoring/top-N.html")
    # y = x.text
    # import pdb; pdb.set_trace()
    morgue_file = fetch_morgue_file(
        morgue_filepath=morgue_filepath,
        morgue_url=morgue_url,
        character=character,
        local_mode=local_mode,
    )
    execute_command(printer, command, morgue_file)


# TODO: I don't like how this has an old_altars input
# since it will never be used, but it does fix the problem
def run_bot(
    server,
    printer,
    morgue_filepath=None,
    morgue_url=None,
    character=None,
    local_mode=None,
    old_altars=None,
):
    while True:
        # We Request the morgue file everytime
        # To get the latest data
        morgue_file = fetch_morgue_file(
            morgue_filepath=morgue_filepath,
            morgue_url=morgue_url,
            character=character,
            local_mode=local_mode,
        )

        # TODO: figure out this ordering
        old_altars, _ = check_for_new_gods(old_altars, morgue_file, printer)

        _respond_to_irc(morgue_file, server, printer)


def _respond_to_irc(morgue_file, server, printer):
    # Change to: restart if files changed
    watch_for_changes()

    # I think we are blocked on waiting for a message here
    # We might want to add a timeout and retry or something
    irc_response = server.recv(2048).decode("utf-8").split()

    # How do we wan to control these prints better
    print(irc_response)

    if len(irc_response) < 2:
        # print(irc_response)
        pass
    elif irc_response[1] == "PRIVMSG":
        process_msg(printer, irc_response, morgue_file)

    # TODO: is the 2nd item in the split IRC response array always the type???
    # What is the IRC RFC???
