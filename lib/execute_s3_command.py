from lib.character import Character
from lib.sns import send_morguefile_notification
from lib.morgue_db import save_a_buncha_info


BAN_LIST = ["JFunk"]


def process_s3_events(event):
    if "Records" in event:
        for record in event["Records"]:
            process_s3_event(record)
    elif "s3" in event:
        process_s3_event(event)


def process_s3_event(event):
    character_name = event["s3"]["object"]["key"].split("/")[0]
    save_a_buncha_info(character_name)

    # How do we stop this in certain scenarios
    character = Character(name=character_name)

    if character_name not in BAN_LIST:
        send_morguefile_notification(character)
    else:
        print(f"Not sending notification for {character_name} new Morgue File")
