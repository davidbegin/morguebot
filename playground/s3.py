import boto3


client = boto3.client("s3")

character = "beginbot"
seed = "10320377110742785619"

morgue_filepath = open("Support/GucciMane.txt").read()


# We Need to find the Pulumi output
bucket_name     = "morgue-files-2944dfb"
key             = f"{character}/{seed}/morguefile.txt"

# TODO: Learn how we can extract this name from Pulumi outputs
# TODO: decide on saving multiple morguefiles, or simply versioning
response = client.put_object(
    ACL='public-read',
    Body=morgue_filepath,
    Bucket=bucket_name,
    Key=key,
)


print(response)


# StorageClass='STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'GLACIER'|'DEEP_ARCHIVE',

