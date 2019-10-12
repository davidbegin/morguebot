from pulumi_aws import dynamodb

dynamodb_table = dynamodb.Table(
    "characters",
    hash_key="character",
    read_capacity=5,
    write_capacity=5,
    attributes=[{"name": "character", "type": "S"}],
)
