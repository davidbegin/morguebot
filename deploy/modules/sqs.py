import pulumi
from pulumi_aws import sqs

gods_queue = sqs.Queue("new-gods-queue", visibility_timeout_seconds=200)
