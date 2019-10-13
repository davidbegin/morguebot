from pulumi_aws import kinesis

chat_stream = kinesis.Stream("twitch-chat", shard_count=2)
