import json

from lib.twitch_chat_bot import send_twitch_message

import boto3
import botocore
import requests

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()


def handler(event, context):
    print(json.dumps(event))
    send_twitch_message(event)
