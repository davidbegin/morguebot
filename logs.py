import json
import time
import subprocess

import boto3
from optparse import OptionParser

client = boto3.client("logs")


def call_bash(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def parse_json(item):
    try:
        return json.loads(item)
    except:
        return None


def monitor_those_logs(log_group, upload_sequence_tokens=[]):
    response = client.describe_log_streams(logGroupName=log_group)
    log_streams = response["logStreams"]

    new_upload_sequence_tokens = [
        log_stream["uploadSequenceToken"] for log_stream in log_streams
    ]

    # for ust in upload_sequence_tokens:
    #     print(ust)
    #     time.sleep(1)

    log_streams = response["logStreams"]
    # log_stream_names = [log_stream['logStreamName'] for log_stream in log_streams]

    for log_stream in log_streams:

        if log_stream["uploadSequenceToken"] in upload_sequence_tokens:
            pass
            # print("OLD MESSAGE!!!!")
        else:
            response = client.get_log_events(
                logGroupName=log_group, logStreamName=log_stream["logStreamName"]
            )
            log_stream_events = response["events"]

            messages = [log_stream["message"] for log_stream in log_stream_events]
            for message in messages:

                if (
                    "START" in message
                    or "END" in message
                    or "REPORT" in message
                    or "ResponseMetadata" in message
                ):
                    # Hard Pass
                    pass
                else:
                    if "ShardId" in message:
                        pass
                    else:
                        if parse_json(message):
                            msg = parse_json(message)
                            if type(msg) is int:
                                pass
                            else:
                                if "Records" in msg:
                                    records = msg["Records"]
                                    if "body" in records[0]:
                                        messages = [
                                            json.loads(record["body"])["Message"]
                                            for record in records
                                        ]
                                        for message in messages:
                                            print(
                                                f"\033[37;1m{log_group}:\033[0m \033[36m{message}\033[0m\n"
                                            )
                                    else:
                                        for record in records:
                                            print(
                                                f"\033[37;1m{log_group}:\033[0m \033[36m{record}\033[0m\n"
                                            )
                                else:
                                    if "notification" in msg:
                                        # SUCCESS
                                        # TODO: Start branching on success
                                        print(f"Notification: {msg['status']}")
                        else:
                            print(f"\033[37m{log_group}:\033[0m {message}")

    time.sleep(1)
    monitor_those_logs(log_group, new_upload_sequence_tokens + upload_sequence_tokens)


def run():
    log_groups = None
    run_count = 0

    while True:
        response = client.describe_log_groups()
        new_log_groups = response["logGroups"]
        log_group_names = [log_group["logGroupName"] for log_group in new_log_groups]

        run_count = run_count + 1
        print(f"Run: {run_count}")
        if log_groups is None:
            log_groups = "safas"
            log_groups = new_log_groups
            print("First Run")
            time.sleep(1)
        else:
            print(len(log_groups))

            if len(new_log_groups) > len(log_groups):
                log_groups = new_log_groups
                print("Hey now we think they are more log groups!")
                time.sleep(1)
                if run_count > 2:
                    # New Tmux window with Log Group
                    command = "tmux split-window -h python logs.py"
                    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
            else:
                log_groups = new_log_groups
                print("Sleeping")
                time.sleep(1)


def destroy():
    response = client.describe_log_groups()
    new_log_groups = response["logGroups"]
    log_group_names = [log_group["logGroupName"] for log_group in new_log_groups]
    for log_group_name in log_group_names:
        response = client.delete_log_group(logGroupName=log_group_name)
        print(log_group_name)


# run()
# destroy()


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
            monitor_those_logs(options.log_group)
        else:
            first_log_group, *other_log_groups = log_group_names

            for log_group_name in other_log_groups:
                command = f"tmux split-window -h python logs.py -l {log_group_name}"
                call_bash(command)

            command = f"tmux resize-pane -D"
            call_bash(command)

            monitor_those_logs(first_log_group)
            # this is the main mode, that will split new log groups
