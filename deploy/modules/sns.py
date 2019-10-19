import json

from pulumi_aws import sns, iam

from modules.iam import CREATE_CW_LOGS_POLICY
from modules.sqs import gods_queue

MODULE_NAME = "gods-queue"

role = iam.Role(
    f"{MODULE_NAME}-topic-role",
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
    f"{MODULE_NAME}-topic",
    sqs_failure_feedback_role_arn=role.arn,
    sqs_success_feedback_role_arn=role.arn,
)
