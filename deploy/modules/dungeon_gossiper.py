import json

import pulumi
from pulumi import Output
from pulumi_aws import iam, lambda_

from modules.dynamodb import dynamodb_table
from modules.sns import sns_topic
from modules.sns import weapons_topic
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from modules.kinesis import chat_stream
from modules.s3 import bucket

MODULE_NAME = "dungeon_gossiper"

config = pulumi.Config()

role = iam.Role(
    f"{MODULE_NAME}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

policy = Output.all(
    dynamodb_table.arn,
    dynamodb_table.stream_arn,
    sns_topic.arn,
    weapons_topic.arn,
    chat_stream.arn,
    bucket.arn,
).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Id": f"{MODULE_NAME}-policy",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {"Effect": "Allow", "Action": ["dynamodb:*"], "Resource": args[0]},
                {"Effect": "Allow", "Action": ["dynamodb:*"], "Resource": args[1]},
                {
                    "Effect": "Allow",
                    "Action": ["sns:*"],
                    "Resource": [args[2], args[3]],
                },
                {"Effect": "Allow", "Action": ["kinesis:*"], "Resource": args[4]},
                {
                    "Effect": "Allow",
                    "Action": ["s3:ListObjectsV2"],
                    "Resource": args[5],
                },
            ],
        }
    )
)

iam.RolePolicyAttachment(
    f"{MODULE_NAME}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=role.id,
)

iam.RolePolicy(f"{MODULE_NAME}-lambda-role-policy", role=role.id, policy=policy)

lambda_variables = Output.all(
    dynamodb_table.name, sns_topic.arn, weapons_topic.arn, chat_stream.name
).apply(
    lambda args: {
        "CHARACTER_DB": args[0],
        "TOPIC_ARN": args[1],
        "WEAPONS_TOPIC": args[2],
        "CHAT_STREAM_NAME": args[3],
    }
)

aws_lambda = lambda_.Function(
    f"{MODULE_NAME}",
    role=role.arn,
    runtime="python3.6",
    handler="lambda_handler.dungeon_gossiper",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    tracing_config={"mode": "Active"},
    environment={"variables": lambda_variables},
)

lambda_.EventSourceMapping(
    f"{MODULE_NAME}-dynamodb-esm",
    event_source_arn=dynamodb_table.stream_arn,
    function_name=aws_lambda.name,
    starting_position="LATEST",
)
