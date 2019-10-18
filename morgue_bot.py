import json

from lib.command_executor import execute_command


import boto3
import botocore
import requests

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()


def handler(event, handler):
    print(json.dumps(event))
    execute_command(event)
