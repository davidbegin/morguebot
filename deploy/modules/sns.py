import json

from pulumi_aws import sns, iam

from modules.iam import CREATE_CW_LOGS_POLICY
from modules.sqs import gods_queue, weapons_queue


role = iam.Role(
    f"topic-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "sns.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }""",
)

sns_topic = sns.Topic(
    f"gods-topic",
    sqs_failure_feedback_role_arn=role.arn,
    sqs_success_feedback_role_arn=role.arn,
)

weapons_topic = sns.Topic(
    f"weapons-topic",
    sqs_failure_feedback_role_arn=role.arn,
    sqs_success_feedback_role_arn=role.arn,
)


sns.TopicSubscription(
    f"weapons-subscription",
    endpoint=weapons_queue.arn,
    protocol="sqs",
    topic=weapons_topic.arn,
)

sns.TopicSubscription(
    f"gods-subscription", endpoint=gods_queue.arn, protocol="sqs", topic=sns_topic.arn
)
