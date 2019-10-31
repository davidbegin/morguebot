
import json
import time
import subprocess
import calendar

import click
import boto3
import durationpy
import datetime
from optparse import OptionParser

def call_bash(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



# arn:aws:kinesis:us-west-2:851075464416:stream/twitch-chat-877759c
if __name__ == "__main__":
    commands = [
            # "lumigo-cli tail-sqs --queueName --region us-west-2",
            # "lumigo-cli tail-sns --topicName gods-topic-gods-topic-f88048a --region us-west-2",
            "lumigo-cli tail-sns --topicName weapons-topic-f819b3f --region us-west-2",
            "lumigo-cli tail-kinesis  --streamName twitch-chat-877759c --region us-west-2",
            ]

    first_command, *other_commands =  commands

    for command in other_commands:
        full_command = f"tmux split-window -h {command}"
        call_bash(full_command)

    command = "tmux select-layout tiled"
    call_bash(first_command)
    # call_bash(first_command)
