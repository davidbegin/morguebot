import json

from pulumi import Output
from pulumi_aws import sqs


def create_queue_policy(name):
    queue = sqs.Queue(f"{name}-queue", visibility_timeout_seconds=200)

    policy = Output.all(queue.arn).apply(
        lambda args: json.dumps(
            {
                "Version": "2012-10-17",
                "Id": f"{name}-policy",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": ["sqs:*"],
                        "Resource": args[0],
                        "Principal": "851075464416",
                    }
                ],
            }
        )
    )

    sqs.QueuePolicy("very-permissive-queue-policy", policy=policy, queue_url=queue.id)

    return queue


weapons_queue = create_queue_policy("weapons")
gods_queue = sqs.Queue("new-gods-queue", visibility_timeout_seconds=200)
xl_upgrades_queue = sqs.Queue("xl-upgrades-queue", visibility_timeout_seconds=200)
