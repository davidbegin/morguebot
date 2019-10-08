import socket
import os

# TODO: Come back and make this configurable
USER = "beginbotbot"


def _handshake(server):
    token = os.environ["TWITCH_OAUTH_TOKEN"]

    # TODO: Come back and make this configurable
    channel = "#beginbot"

    server.send(bytes("PASS " + token + "\r\n", "utf-8"))
    server.send(bytes("NICK " + USER + "\r\n", "utf-8"))
    server.send(bytes("JOIN " + channel + "\r\n", "utf-8"))


def connect_to_twitch():
    connection_data = ("irc.chat.twitch.tv", 6667)
    server = socket.socket()
    server.connect(connection_data)
    _handshake(server)
    return server
