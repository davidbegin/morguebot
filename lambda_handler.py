import os
import json

import boto3
import botocore
import requests

if os.environ.get("AWS_LAMBDA_FUNCTION_NAME", None):
    from aws_xray_sdk.core import xray_recorder
    from aws_xray_sdk.core import patch_all

    patch_all()

from lib.twitch_chat_bot import send_twitch_message
from lib.command_executor import execute_command
from lib.morgue_stalker import stalk
from lib.god_bot import monitor_the_gods


def morgue_stalker(event, handler):
    print(json.dumps(event))
    stalk(event)


def twitch_chat_bot(event, context):
    print(json.dumps(event))
    send_twitch_message(event)


def morgue_bot(event, handler):
    print(json.dumps(event))
    execute_command(event)


def god_bot(event, context):
    print(json.dumps(event))
    monitor_the_gods(event)


def xl_bot(event, handler):
    print("I'm xl_bot!")
