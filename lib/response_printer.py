import json


def print_response(response, msg, description):
    metadata = response["ResponseMetadata"]
    status = metadata["HTTPStatusCode"]

    if status == 200:
        print(f"\033[35m{description}: {msg}...\033[0m")
    else:
        print(f"\033[31m{json.dumps(response)}\033m")
