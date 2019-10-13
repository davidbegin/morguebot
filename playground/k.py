import json
import boto3

# WE need to write ot that kinesis stream

# Thats it

client = boto3.client("kinesis")

kinesis_arn = "arn:aws:kinesis:us-west-2:851075464416:stream/twitch-chat-f5f8ef7"
kinesis_name= "twitch-chat-f5f8ef7"

response = client.put_record(
    StreamName=kinesis_name,
    Data=json.dumps({"name":"begin", "message": "Testing with Kinesis!"}),
    PartitionKey='alpha',
)

print(response)


# # shard_id=response["ShardId"]
# # print(f"Shard ID: {shard_id}"

# shard_id="shardId-000000000000"

# print("\n---\n")

# response = client.get_shard_iterator(
#     StreamName=kinesis_name,
#     ShardId=shard_id,
#     ShardIteratorType='TRIM_HORIZON'
# )

# # print(response)
# # print("\n---\n")

# shard_iterator = response["ShardIterator"]

# response = client.get_records(ShardIterator=shard_iterator)

# print(response)



