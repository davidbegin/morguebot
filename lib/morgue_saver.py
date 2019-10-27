import os
import boto3

MORGUE_BUCKETNAME = os.environ.get("MORGUE_BUCKETNAME", "morgue-files-2944dfb")


def morgue_saver(character, morgue):
    client = boto3.client("s3")

    key = f"{character.name}/morguefile.txt"

    old_saved_morgue = character.s3_morgue_file()

    if morgue != old_saved_morgue:
        print(f"Fresh Morgue File for {character.name}")
        # TODO: Learn how we can extract this name from Pulumi outputs
        # TODO: decide on saving multiple morguefiles, or simply versioning
        response = client.put_object(
            ACL="public-read", Body=morgue, Bucket=MORGUE_BUCKETNAME, Key=key
        )
        print(response)
    else:
        print(f"Identical Morgue for {character.name}")
