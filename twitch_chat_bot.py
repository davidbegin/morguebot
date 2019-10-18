import json

from lib.twitch_chat_bot import send_twitch_message


def handler(event, context):
    print(json.dumps(event))
    send_twitch_message(event)
