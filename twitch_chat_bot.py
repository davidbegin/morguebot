from lib.twitch_bot_chat import send_twitch_message


def handler(event, context):
    print(json.dumps(event))
    send_twitch_message(event)
