import socket
import os
import boto3
from base64 import b64decode


def _handshake(server):
    # TODO: add error handling around not having the required environment variables
    # TODO: add some conncection debug information
    if "AWS_LAMBDA_NAME" in os.environ:
        encrypted_token = os.environ["MORGUEBOT_TWITCH_OAUTH_TOKEN"]
        token = boto3.client("kms").decrypt(CiphertextBlob=b64decode(encrypted_token))[
            "Plaintext"
        ]
    else:
        token = os.environ["MORGUEBOT_TWITCH_OAUTH_TOKEN"]
    bot = os.environ["MORGUEBOT_BOT_NAME"]
    channel = os.environ["MORGUEBOT_CHANNEL"]

    server.send(bytes("PASS " + token + "\r\n", "utf-8"))
    server.send(bytes("NICK " + bot + "\r\n", "utf-8"))
    server.send(bytes("JOIN " + f"#{channel}" + "\r\n", "utf-8"))


def connect_to_twitch():
    connection_data = ("irc.chat.twitch.tv", 6667)
    server = socket.socket()
    server.connect(connection_data)
    _handshake(server)
    return server
