from lib.sns import send_morguefile_notification
from lib.morgue_db import save_a_buncha_info


def process_s3_events(event):
    if "Records" in event:
        for record in event["Records"]:
            process_s3_event(record)
    elif "s3" in event:
        process_s3_event(event)


def process_s3_event(event):
    character = event["s3"]["object"]["key"].split("/")[0]
    save_a_buncha_info(character)

    # How do we stop this in certain scenarios
    # send_morguefile_notification(character)
