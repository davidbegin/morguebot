import pulumi
from pulumi import Output
import json
from modules.s3 import bucket
from modules.kinesis import chat_stream
from modules.sqs import gods_queue
from pulumi_aws import iam, lambda_
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from modules.dynamodb import dynamodb_table

config = pulumi.Config()

module_name = "god-bot"

s3_lambda_role = iam.Role(
    f"{module_name}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

lambda_role_policy = Output.all(bucket.arn, gods_queue.arn, chat_stream.arn).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Id": f"{module_name}-policy",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {"Effect": "Allow", "Action": ["s3:PutObject"], "Resource": args[0]},
                {"Effect": "Allow", "Action": ["sqs:*"], "Resource": args[1]},
                {
                    "Effect": "Allow",
                    "Action": ["kinesis:PutRecord"],
                    "Resource": args[2],
                },
            ],
        }
    )
)


iam.RolePolicyAttachment(
    f"{module_name}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=s3_lambda_role.id,
)

lambda_role_policy = iam.RolePolicy(
    f"{module_name}-lambda-role-policy",
    role=s3_lambda_role.id,
    policy=lambda_role_policy,
)

# source_code_hash=None
# https://morgue-artifacts.s3-us-west-2.amazonaws.com/handler.zip
# TODO: Add the source_hash_code thang to trigger updates
cloudwatch_lambda = lambda_.Function(
    f"{module_name}",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="god_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    tracing_config={"mode": "Active"},
    environment={
        "variables": {
            "CHARACTER_DB": dynamodb_table.name,
            "MORGUE_BUCKETNAME": bucket.id,
            "CHAT_STREAM_ARN": chat_stream.arn,
            "CHAT_STREAM_NAME": chat_stream.name,
        }
    },
)

lambda_.EventSourceMapping(
    f"{module_name}-sqs-esm",
    event_source_arn=gods_queue.arn,
    function_name=cloudwatch_lambda.name,
    # starting_position="AT_TIMESTAMP",
    # starting_position_timestamp="AT_TIMESTAMP",
)

# def __init__(batch_size=None, enabled=None,
#         starting_position=None, starting_position_timestamp=None, __props__=None, __name__=None, __opts__=None):
