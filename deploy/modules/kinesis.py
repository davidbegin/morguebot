from pulumi_aws import kinesis

chat_stream = kinesis.Stream("twitch-chat", shard_count=2)

error_stream = kinesis.Stream("error-chat", shard_count=2)
