import os
import boto3

MORGUE_BUCKETNAME = os.environ.get("MORGUE_BUCKETNAME", "morgue-files-2944dfb")


def morgue_saver(character, morgue, refresh=False):
    client = boto3.client("s3")

    key = f"{character.name}/morguefile.txt"

    old_saved_morgue = character.s3_morgue_file()

    if morgue != old_saved_morgue or refresh:
        print(f"Fresh Morgue File for {character.name}")
        # TODO: Learn how we can extract this name from Pulumi outputs
        # TODO: decide on saving multiple morguefiles, or simply versioning
        response = client.put_object(
            ACL="public-read", Body=morgue, Bucket=MORGUE_BUCKETNAME, Key=key
        )
        metadata = response["ResponseMetadata"]
        status = metadata["HTTPStatusCode"]
        if status == 200:
            print("\033[37mObject safely stored in S3\033[0m")
        else:
            print(response)
    else:
        print(f"\033[33mIdentical Morgue for {character.name}\033[0m")
