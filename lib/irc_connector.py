import json
import socket
import os
import boto3
from base64 import b64decode


def _handshake(server):
    # TODO: add error handling around not having the required environment variables
    # TODO: add some connection debug information
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        encrypted_token = os.environ["MORGUEBOT_TWITCH_OAUTH_TOKEN"]
        raw_token = boto3.client("kms").decrypt(
            CiphertextBlob=b64decode(encrypted_token)
        )["Plaintext"]
        token = str(raw_token, "UTF-8")
    else:
        token = os.environ["MORGUEBOT_TWITCH_OAUTH_TOKEN"]

    bot = os.environ["MORGUEBOT_BOT_NAME"]
    channel = os.environ["MORGUEBOT_CHANNEL"]

    # print(json.dumps({"message": f"Connecting to #{channel} as {bot}"}))

    server.send(bytes("PASS " + token + "\r\n", "utf-8"))
    server.send(bytes("NICK " + bot + "\r\n", "utf-8"))
    server.send(bytes("JOIN " + f"#{channel}" + "\r\n", "utf-8"))


def connect_to_twitch():
    if "MORGUEBOT_TWITCH_OAUTH_TOKEN" in os.environ:
        connection_data = ("irc.chat.twitch.tv", 6667)
        server = socket.socket()
        server.connect(connection_data)
        _handshake(server)
        return server
    else:
        print("Not connecting to Twitch")
