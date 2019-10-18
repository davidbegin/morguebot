import json

import pulumi
from pulumi_aws import sns, iam

from modules.iam import CREATE_CW_LOGS_POLICY
from modules.sqs import gods_queue

module_name = "gods-queue"

god_queue_topic_role = iam.Role(
    f"{module_name}-topic-role",
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
    f"{module_name}-topic",
    sqs_failure_feedback_role_arn=god_queue_topic_role.arn,
    sqs_success_feedback_role_arn=god_queue_topic_role.arn,
)

pulumi.export("sns_topic_arn", sns_topic.arn)
