import pulumi
from pulumi_aws import dynamodb


dynamodb_table = dynamodb.Table(
    "crawl-characters",
    hash_key="character",
    read_capacity=5,
    write_capacity=5,
    attributes=[{"name": "character", "type": "S"}],
    stream_enabled=True,
    stream_view_type="NEW_AND_OLD_IMAGES",
)
