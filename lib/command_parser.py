import json

import boto3

from lib.printer import Printer


RESISTANCES = ["!rF", "!rFire", "!rCold", "!rNeg", "!rPois", "!rE", "!rElec", "!rCorr"]
TRAITS = ["!SeeInvis", "!Gourm", "!Faith", "!Spirit", "!Reflect", "!Harm"]
COMMANDS_WITH_NO_ARGS = (
    [
        "!overview",
        "!mr",
        "!stlth",
        "!mutations",
        "!jewellery",
        "!scrolls",
        "!potions",
        "!weapons",
        "!armour",
        "!skills",
        "!spells",
        "!h?",
        "!maxR",
        "!mf",
        "!gods",
    ]
    + RESISTANCES
    + TRAITS
)


def process_msg(printer, irc_response, character):
    user, msg = _parse_user_and_msg(irc_response)

    if _is_command_msg(msg):
        split_command = msg.split()
        command = split_command[0]

        if len(split_command) > 1:
            character_name = split_command[1]
        else:
            character_name = character.character

        invoke_morgue_bot(character_name, command)
    else:
        print(f"\033[37;1m{user}:\033[0m {msg}")


def invoke_morgue_bot(character, command):
    print("invoke_morgue_bot")
    client = boto3.client("lambda")

    payload = {"character": character, "command": command}
    client.invoke(FunctionName="morgue-bot-2fc463f", Payload=json.dumps(payload))


def execute_command(printer, msg, character):
    morgue_file = character.morgue_file()
    split_command = msg.split()
    command = split_command[0]

    # TODO: Start account for commands with args

    # TODO: we need to be checking the commands against Aliases here
    if command in COMMANDS_WITH_NO_ARGS:
        if command == "!overview":
            printer.print_overview(morgue_file)
        elif command in RESISTANCES:
            printer.print_resistance(command[1:], morgue_file)
        elif command in TRAITS:
            printer.print_traits(command, morgue_file)
        elif command == "!h?":
            printer.print_help(COMMANDS_WITH_NO_ARGS)
        elif command == "!skills":
            printer.print_skills(morgue_file)
        elif command == "!weapons":
            printer.print_weapons(morgue_file)
        elif command == "!armour":
            printer.print_armour(morgue_file)
        elif command == "!potions":
            printer.print_potions(morgue_file)
        elif command == "!jewellery":
            printer.print_jewellery(morgue_file)
        elif command == "!scrolls":
            printer.print_scrolls(morgue_file)
        elif command == "!mutations":
            printer.print_mutations(morgue_file)
        elif command == "!stlth":
            printer.print_stealth(morgue_file)
        elif command == "!mr":
            printer.print_mr(morgue_file)
        elif command == "!maxR":
            printer.print_max_resistance(morgue_file)
        elif command == "!gods":
            printer.print_gods(morgue_file)
        elif command == "!spells":
            printer.print_spells(morgue_file)
        elif command == "!mf":
            pass
            # printer.print_morgue_file_location(morgue_file)
    else:
        print(f"\033[31;1mINVALID COMMAND: {command}\033[0m")
        print(f"Valid Commands: {COMMANDS_WITH_NO_ARGS}")
        # TODO: Configure this to be on or off
        printer.print_help(COMMANDS_WITH_NO_ARGS)


# TODO: refactor this sillyness
def _parse_user_and_msg(irc_response):
    user_info, _, _, *raw_msg = irc_response
    raw_first_word, *raw_rest_of_the_message = raw_msg
    first_word = raw_first_word[1:]
    rest_of_the_message = " ".join(raw_rest_of_the_message)
    user = user_info.split("!")[0][1:]
    msg = f"{first_word} {rest_of_the_message}"
    return user, msg


def _is_command_msg(msg):
    return msg[0] == "!" and msg[1] != "!"
