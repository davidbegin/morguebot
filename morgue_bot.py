import json

from lib.command_executor import execute_command


def handler(event, handler):
    print(json.dumps(event))
    execute_command(event)
