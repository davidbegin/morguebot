import json
import time
import subprocess
import calendar

import click
import boto3
import durationpy
import datetime
from optparse import OptionParser

client = boto3.client("logs")

def _filter_out_xray_warnings(events):
    # log_strs = ["START", "REPORT", "END"]
    log_strs = ["START", "END"]

    return list(
        filter(
            lambda event: all(log_str not in event["message"] for log_str in log_strs),
            events,
        )
    )


def convert_from_epoch(unix_time: int) -> str:
    return time.strftime("%Y-%m-%d %I:%M:%S %p %Z", time.localtime(unix_time / 1000))


def _print_events(log_group_name, events) -> None:
    for event in events:
        if "[ERROR]" in event["message"]:
            fg_color = "red"
            nl = True
        elif "[WARNING]" in event["message"]:
            fg_color = "yellow"
            nl = True
        else:
            fg_color = "green"
            nl = False

        formatted_log_group_name = log_group_name
        _print_event(
            formatted_log_group_name, event["timestamp"], event["message"], fg_color, nl
        )


# Kinesis Messsage
# SNS Message VIA SQS Messaage
# S3 Message
# Regular Event???

def is_kinesis_message(message):
    return True
    # We need to figure out what the heck is a Kinesis Message


def _print_event(log_group_name, timestamp, message, fg_color, nl):

    # if is_kinesis_message(message):
    #     print("KINESIISSISISISISISI")

    formatted_timestamp = convert_from_epoch(timestamp)
    click.echo(
        f"{click.style(f'💌 {log_group_name} | ', bold=True, fg='white')}"
        f"{click.style(f'{formatted_timestamp} | ', fg='cyan')}"
        f"{click.style(f'{message}', fg=fg_color)}",
        nl=nl,
    )


def _fetch_log_steam_names(log_group_name):
    try:
        response = client.describe_log_streams(
            logGroupName=log_group_name, descending=True, orderBy="LastEventTime"
        )

        log_streams = response["logStreams"]
        return [stream["logStreamName"] for stream in log_streams]
    except Exception as e:
        print(f"Error calling describe_log_streams: {e}")
        return None


def monitor_those_logs(log_group):
    filter_pattern = ""
    limit = 10000
    duration_str = "5m"
    print_header = False

    stream_names = _fetch_log_steam_names(log_group)

    if not stream_names:
        return None

    response = {}
    events = []

    while not response or "nextToken" in response:
        start_time = _convert_duration_string_to_time_delta(duration_str)
        extra_args = {}
        if "nextToken" in response:
            extra_args["nextToken"] = response["nextToken"]

        end_time = int(time.time()) * 1000

        response = client.filter_log_events(
            logGroupName=log_group,
            logStreamNames=stream_names,
            startTime=start_time,
            endTime=end_time,
            filterPattern=filter_pattern,
            limit=limit,
            interleaved=True,
        )
        if response and "events" in response:
            events += response["events"]

    events = _filter_out_xray_warnings(events)

    if events:
        _print_events(log_group, events)
        # print(f"\033[36;1m{log_group}:\033[0m {events}")


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


def sanitize_those_cw_names(log_group_name):
    if "/aws/lambda" in log_group_name:
        return log_group_name.replace("/aws/lambda", "")
    else:
        return log_group_name

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

        if options.log_group:
            command = "tmux select-layout tiled"
            call_bash(command)
            print(f"\033[37m{sanitize_those_cw_names(options.log_group)}\033[0m")
            while True:
                monitor_those_logs(options.log_group)
                time.sleep(2)
        else:
            # We should take these in from command Land Args in JSON
            log_group_names = [
		# "/aws/lambda/morgue-stalker-341e60e",
		# "/aws/lambda/morgue-bot-2fc463f",
                # 'API-Gateway-Execution-Logs_zl5r1fjaxf/Stage',
                # '/aws/lambda/lambda-authorizer',
                # '/aws/lambda/xl-bot-00f604b',
                # '/aws/lambda/dungeon-gossiper-284d48b',
                # '/aws/lambda/weapons-bot-b08077f',
		"/aws/lambda/destinations-lambda-a2f8fc7",
                # "/aws/lambda/god-bot-62a15fe",
		# "/aws/lambda/twitch-chat-bot-82104fd",
            ]

            first_log_group, *other_log_groups = log_group_names

            for log_group_name in other_log_groups:
                command = f"tmux split-window -h python logs.py -l {log_group_name}"
                call_bash(command)

            command = "tmux select-layout tiled"
            call_bash(command)
            print(f"\033[37m{sanitize_those_cw_names(first_log_group)}\033[0m")
            while True:
                monitor_those_logs(first_log_group)
                time.sleep(1)
