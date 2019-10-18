import pulumi
from pulumi_aws import dynamodb


dynamodb_table = dynamodb.Table(
    "characters",
    hash_key="character",
    read_capacity=5,
    write_capacity=5,
    attributes=[{"name": "character", "type": "S"}],
)

pulumi.export("dyanmodb_table", dynamodb_table.name)
