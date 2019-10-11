import os
import boto3


def morgue_saver(character, morgue):
    client = boto3.client("s3")

    # We Need to find the Pulumi output
    key = f"{character.character}/morguefile.txt"

    # TODO: Learn how we can extract this name from Pulumi outputs
    # TODO: decide on saving multiple morguefiles, or simply versioning
    response = client.put_object(
        ACL="public-read", Body=morgue, Bucket=os.environ["MORGUE_BUCKETNAME"], Key=key
    )

    print(response)

    # StorageClass='STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'GLACIER'|'DEEP_ARCHIVE',
