mport json
import boto3

# WE need to write ot that kinesis stream

# Thats it

# client = boto3.client("kinesis")
client = boto3.client("sns")


topic_arn = "arn:aws:sns:us-west-2:851075464416:god-queue-topic-a3644eb"
# msg = {"message": "Testing From SNS to SQS to Kinsesis!"}
msg = json.dumps({"default": "We are getting closer"})
response = client.publish(
    TopicArn=topic_arn,
    Message=msg,
    MessageStructure='json',

    # Subject='Testing',
    # MessageAttributes={
    #     'string': {
    #         'DataType': 'string',
    #         'StringValue': 'string',
    #         'BinaryValue': b'bytes'
    #     }
    # }
)

print(response)

# {
#   "Records": [
#     {
#       "EventSource": "aws:sns",
#       "EventVersion": "1.0",
#       "EventSubscriptionArn": "arn:aws:sns:us-west-2:{{{accountId}}}:ExampleTopic",
#       "Sns": {
#         "Type": "Notification",
#         "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
#         "TopicArn": "arn:aws:sns:us-west-2:123456789012:ExampleTopic",
#         "Subject": "example subject",
#         "Message": "example message",
#         "Timestamp": "1970-01-01T00:00:00.000Z",
#         "SignatureVersion": "1",
#         "Signature": "EXAMPLE",
#         "SigningCertUrl": "EXAMPLE",
#         "UnsubscribeUrl": "EXAMPLE",
#         "MessageAttributes": {
#           "Test": {
#             "Type": "String",
#             "Value": "TestString"
#           },
#           "TestBinary": {
#             "Type": "Binary",
#             "Value": "TestBinary"
#           }
#         }
#       }
#     }
#   ]
# }


def sqs():
    client = boto3.client("sqs")
    sqs_arn = "arn:aws:sqs:us-west-2:851075464416:new-gods-queue-6fecb43"

    msg = json.dumps({"message": "Testing with SQS!"})
    sqs_url = "https://sqs.us-west-2.amazonaws.com/851075464416/new-gods-queue-6fecb43"

    client.send_message(QueueUrl=sqs_url, MessageBody=msg)


# kinesis_arn = "arn:aws:kinesis:us-west-2:851075464416:stream/twitch-chat-f5f8ef7"
# kinesis_name= "twitch-chat-f5f8ef7"

# response = client.put_record(
#     StreamName=kinesis_name,
#     Data=json.dumps({"name":"begin", "message": "Testing with Kinesis!"}),
#     PartitionKey='alpha',
# )

# print(response)


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



