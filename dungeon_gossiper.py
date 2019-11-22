from lib.command_executor import print_the_help
from lib.command_executor import Formatter
from lib.kinesis import send_chat_to_stream
from lib.morgue_saver import morgue_saver
from lib.character import Character

from flask_app import app


@app.route("/xl-bot/gossip")
def gossip():
    return "DID YOU HEARRRRR"
