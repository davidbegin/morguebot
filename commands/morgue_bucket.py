import os

import boto3


BUCKET_NAME = os.environ.get("MORGUE_BUCKETNAME", "morgue-files-2944dfb")

def clear(logger):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    response = bucket.objects.all().delete()
    logger.info(f"Deleted Objects from {BUCKET_NAME}", response=response)

