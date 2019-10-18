import pulumi
from pulumi_aws import kinesis

chat_stream = kinesis.Stream("twitch-chat", shard_count=2)

pulumi.export("kinesis_arn", chat_stream.arn)
