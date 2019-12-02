import json

from pulumi import Output
from pulumi_aws import sqs


def create_queue_and_policy(name):
    queue = sqs.Queue(f"{name}-queue", visibility_timeout_seconds=200)

    policy = Output.all(queue.arn).apply(
        lambda args: json.dumps(
            {
                "Version": "2012-10-17",
                "Id": f"{name}-policy",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": ["SQS:*"],
                        "Resource": args[0],
                        "Principal": "*",
                    }
                ],
            }
        )
    )

    sqs.QueuePolicy(f"{name}-very-permissive", policy=policy, queue_url=queue.id)

    return queue


errors_queue = create_queue_and_policy("errors")
weapons_queue = create_queue_and_policy("weapons")
gods_queue = create_queue_and_policy("gods")
xl_upgrades_queue = create_queue_and_policy("xl")
