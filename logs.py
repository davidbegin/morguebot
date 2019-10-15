import json
import time
import subprocess
import calendar

import boto3
import durationpy
import datetime
from optparse import OptionParser

client = boto3.client("logs")


def _fetch_log_steam_names(log_group_name: str):
    try:
        response = client.describe_log_streams(
                logGroupName=log_group_name,
                descending=True,
                orderBy='LastEventTime'
                )

        log_streams = response["logStreams"]
        return [stream['logStreamName'] for stream in log_streams]
    except Exception as e:
        print(f"Error calling describe_log_streams: {e}")
        return None

def monitor_those_logs(log_group):
    filter_pattern = ""
    limit = 10000
    duration_str = "5m"
    print_header = False
    start_time = _convert_duration_string_to_time_delta(duration_str)

    stream_names = _fetch_log_steam_names(log_group)

    if not stream_names:
        return None

    response = {}
    events = []

    while not response or 'nextToken' in response:
        extra_args = {}
        if 'nextToken' in response:
            extra_args['nextToken'] = response['nextToken']

        end_time = int(time.time()) * 1000

        response = client.filter_log_events(
                logGroupName=log_group,
                logStreamNames=stream_names,
                startTime=start_time,
                endTime=end_time,
                filterPattern=filter_pattern,
                limit=limit,
                interleaved=True
        )
        if response and 'events' in response:
            events += response['events']

    if events:
        print(events)

def _convert_duration_string_to_time_delta(duration_str: str) -> int:
    delta = durationpy.from_str(duration_str)
    past = datetime.datetime.utcnow() - delta
    return calendar.timegm(past.timetuple()) * 1000


def call_bash(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def parse_json(item):
    try:
        return json.loads(item)
    except:
        return None

def destroy():
    response = client.describe_log_groups()
    new_log_groups = response["logGroups"]
    log_group_names = [log_group["logGroupName"] for log_group in new_log_groups]
    for log_group_name in log_group_names:
        response = client.delete_log_group(logGroupName=log_group_name)
        print(log_group_name)


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-d", "--destroy", action="store_true", dest="destroy")
    parser.add_option("-l", "--log-group", type="string", dest="log_group")
    (options, args) = parser.parse_args()

    if options.destroy:
        destroy()
    else:
        response = client.describe_log_groups()
        new_log_groups = response["logGroups"]
        log_group_names = [log_group["logGroupName"] for log_group in new_log_groups]

        for log_group_name in log_group_names:
            print(log_group_name)

        if options.log_group:
            command = "tmux select-layout tiled"
            call_bash(command)
            while True:
                monitor_those_logs(options.log_group)
                time.sleep(2)
        else:
            first_log_group, *other_log_groups = log_group_names

            for log_group_name in other_log_groups:
                command = f"tmux split-window -h python logs.py -l {log_group_name}"
                call_bash(command)

            commmand = "tmux select-layout tiled"
            call_bash(command)
            monitor_those_logs(first_log_group)


