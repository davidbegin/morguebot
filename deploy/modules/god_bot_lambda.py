import pulumi
from pulumi import Output
import json
from modules.s3 import bucket
from modules.kinesis import chat_stream
from modules.sqs import gods_queue
from pulumi_aws import iam, lambda_
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY

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
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)
