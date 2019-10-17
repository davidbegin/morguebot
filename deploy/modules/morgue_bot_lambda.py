from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from modules.sns import sns_topic
from modules.kinesis import chat_stream
from modules.s3 import bucket
from modules.sqs import gods_queue
from modules.dynamodb import dynamodb_table

import json

from pulumi_aws import iam, lambda_
import pulumi
from pulumi import Output

config = pulumi.Config()

module_name = "morgue-bot"

morgue_parser_lambda_role = iam.Role(
    f"{module_name}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

lambda_role_policy = Output.all(
    bucket.arn, sns_topic.arn, dynamodb_table.arn, chat_stream.arn
).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {"Effect": "Allow", "Action": ["s3:*"], "Resource": args[0]},
                {"Effect": "Allow", "Action": ["sns:Publish"], "Resource": args[1]},
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                    ],
                    "Resource": args[2],
                },
                {
                    "Effect": "Allow",
                    "Action": ["kinesis:PutRecord"],
                    "Resource": args[3],
                },
            ],
        }
    )
)

iam.RolePolicyAttachment(
    f"{module_name}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=morgue_parser_lambda_role.id,
)
morgue_parser_lambda_role_policy = iam.RolePolicy(
    f"{module_name}-lambda-role-policy",
    role=morgue_parser_lambda_role.id,
    policy=lambda_role_policy,
)

# TODO: Add the source_hash_code thang to trigger updates
morgue_parser_lambda = lambda_.Function(
    f"{module_name}",
    role=morgue_parser_lambda_role.arn,
    runtime="python3.6",
    handler="morgue_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    tracing_config={"mode": "Active"},
    environment={
        "variables": {
            "CHARACTER_DB": dynamodb_table.name,
            "TOPIC_ARN": sns_topic.arn,
            "MORGUE_BUCKETNAME": bucket.id,
            "CHAT_STREAM_ARN": chat_stream.arn,
            "CHAT_STREAM_NAME": chat_stream.name,
        }
    },
)

lambda_.Permission(
    "AllowInvocationFromMorgueFileBucket",
    action="lambda:InvokeFunction",
    function=morgue_parser_lambda.arn,
    principal="s3.amazonaws.com",
    source_arn="arn:aws:s3:::morgue-files-2944dfb",
)
