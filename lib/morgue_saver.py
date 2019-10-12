import os
import boto3


def morgue_saver(character, morgue):
    if "MORGUE_BUCKETNAME" in os.environ:
        client = boto3.client("s3")

        # We Need to find the Pulumi output
        key = f"{character.character}/morguefile.txt"

        # TODO: Learn how we can extract this name from Pulumi outputs
        # TODO: decide on saving multiple morguefiles, or simply versioning
        response = client.put_object(
            ACL="public-read",
            Body=morgue,
            Bucket=os.environ["MORGUE_BUCKETNAME"],
            Key=key,
        )

        print(response)
    else:
        print(
            "Not saving Morgue File to S3. Please set MORGUE_BUCKETNAME env var to do so."
        )
