#!/usr/bin/env python3

import argparse
import asyncio
import getpass
import logging
import json
import os
import os.path
import re
import sys
from urllib.parse import urlparse
from webtiles import WebTilesConnection
from webtiles import WebTilesGameConnection


_log = logging.getLogger()
_log.setLevel(logging.INFO)
_log.addHandler(logging.StreamHandler())


class TryThisOut(WebTilesGameConnection):
    def __init__(self, websocket_url, username, password, protocol_version):
        super().__init__()
        self.websocket_url = websocket_url
        self.username = username
        self.password = password
        self.protocol_version = protocol_version

    @asyncio.coroutine
    def start(self):
        """Connect to the WebTiles server, then proceed to read and handle
        messages. When the game list is received, try to update the RC file.

        """

        yield from self.connect(
            self.websocket_url, self.username, self.password, self.protocol_version
        )

        while True:
            messages = yield from self.read()

            if not messages:
                return

            for message in messages:
                yield from self.handle_message(message)

            # if not self.games:
            #     continue

            if not self.lobby_entries:
                continue

            print("We found the lobby_entries!")

            # {'username': 'beginbot', 'xl': '11', 'title': 'Fighter', 'spectator_count': 0, 'god': 'Trog', 'idle_time': 395, 'char': 'MiBe', 'place': 'Orc:1', 'msg': 'lobby_entry', 'game_id': 'dcss-git', 'id': 23981, 'time_last_update': 1572572963.860949}
            with open("tmp/lobby_entries.json", "w") as f:
                f.write(json.dumps({"entries": self.lobby_entries}))

            yield from self.disconnect()
            return

    def handle_message(self, message):
        yield from super().handle_message(message)

        if message["msg"] == "login_fail":
            yield from self.disconnect()
            raise Exception("Login failed.")


@asyncio.coroutine
def try_this_out(username, password):
    print("inside Try this out")
    url = "ws://crawl.akrasiac.org:8080/socket"
    protocol_version = 1
    hostname = urlparse(url).hostname
    # _log.info("Updating server %s", hostname)
    updater = TryThisOut(url, username, password, protocol_version)

    try:
        yield from updater.start()
    except Exception as e:
        err_reason = type(e).__name__
        if e.args:
            err_reason = e.args[0]
        _log.error("Unable to update RC at %s: %s", url, err_reason)
        sys.exit(1)


# _log.info("Updates complete")


def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-u",
        dest="username",
        metavar="<username>",
        help="The account username.",
        default=None,
    )
    parser.add_argument(
        "-p",
        dest="password",
        metavar="<password>",
        help="The account password.",
        default=None,
    )
    args = parser.parse_args()

    username = args.username
    if not username:
        while not username:
            try:
                username = input("Crawl username: ")
            except:
                sys.exit(1)

    password = args.password
    if not password:
        while not password:
            try:
                password = os.environ["CRAWL_PASSWORD"]
            except:
                import pdb

                pdb.set_trace()
                sys.exit(1)

    # _log.info("Updates complete")
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(try_this_out(username, password))


if __name__ == "__main__":
    exit(main())
