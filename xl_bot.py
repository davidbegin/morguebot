from lib.command_executor import print_the_help
from lib.command_executor import Formatter
from lib.kinesis import send_chat_to_stream
from lib.morgue_saver import morgue_saver
from lib.character import Character

from flask_app import app


@app.route("/xl-bot/runes/<name>")
def runes(name):
    character = Character(name=name)
    formatter = Formatter(character)
    msg = formatter.print_runes()
    if msg:
        send_chat_to_stream(msg)
        return " ".join(msg)
    else:
        return "No Runes Found!"


@app.route("/xl-bot/help")
def help():
    logger = None
    print_the_help(logger)
    return "We Helped!"


@app.route("/xl-bot/fetch/<name>")
def fetch(name):
    character = Character(name=name)
    morgue_saver(character, character.non_saved_morgue_file(), True)
    return f"Fetched {name}'s Morgue File!"


# Should we have it /name/command or /command/name
@app.route("/xl-bot/weapons/<name>")
def weapons(name):
    character = Character(name=name)
    formatter = Formatter(character)
    msg = formatter.print_weapons()
    if msg:
        send_chat_to_stream(msg)
        return " ".join(msg)
    else:
        return "No Weapons Found!"
