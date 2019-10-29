
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


if __name__ == "__main__":
    commands = [
            "lumigo-cli tail-sqs --queueName entitlement-seat_transform-olivia --region us-west-2",
            "lumigo-cli tail-sns --topicName async-events-olivia --region us-west-2",
            "lumigo-cli tail-kinesis  --streamName event-stream-rival-olivia --region us-west-2",
            ]

    # first_command, *other_commands =  commands

    for command in commands:
        full_command = f"tmux split-window -h {command}"
        call_bash(full_command)

    command = "tmux select-layout tiled"
    call_bash(command)
    # call_bash(first_command)
