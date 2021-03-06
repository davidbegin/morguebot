import json

from pulumi_aws import iam, lambda_, s3
import pulumi
from pulumi import Output

from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from modules.sns import sns_topic
from modules.sns import weapons_topic
from modules.kinesis import chat_stream
from modules.s3 import bucket
from modules.sqs import gods_queue
from modules.dynamodb import dynamodb_table
from modules.layers import dependency_layer


MODULE_NAME = "morgue-bot"

config = pulumi.Config()


role = iam.Role(
    f"{MODULE_NAME}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

policy = Output.all(
    bucket.arn, sns_topic.arn, weapons_topic.arn, dynamodb_table.arn, chat_stream.arn
).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {"Effect": "Allow", "Action": ["s3:Get*"], "Resource": args[0]},
                {
                    "Effect": "Allow",
                    "Action": ["sns:Publish"],
                    "Resource": [args[1], args[2]],
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:scan",
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                    ],
                    "Resource": args[3],
                },
                {
                    "Effect": "Allow",
                    "Action": ["kinesis:PutRecord"],
                    "Resource": args[4],
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
    dynamodb_table.name, bucket.id, chat_stream.arn, chat_stream.name, sns_topic.arn
).apply(
    lambda args: {
        "CHARACTER_DB": args[0],
        "MORGUE_BUCKETNAME": args[1],
        "CHAT_STREAM_ARN": args[2],
        "CHAT_STREAM_NAME": args[3],
        "TOPIC_ARN": args[4],
    }
)

aws_lambda = lambda_.Function(
    f"{MODULE_NAME}",
    role=role.arn,
    runtime="python3.6",
    handler="lambda_handler.morgue_bot",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    tracing_config={"mode": "Active"},
    environment={"variables": lambda_variables},
    layers=[dependency_layer.arn],
)

lambda_.Permission(
    "AllowInvocationFromMorgueFileBucket",
    action="lambda:InvokeFunction",
    function=aws_lambda.arn,
    principal="s3.amazonaws.com",
    source_arn=bucket.arn,
)

s3.BucketNotification(
    f"{MODULE_NAME}-new-morgue-files",
    bucket=bucket.id,
    lambda_functions=[
        {"events": ["s3:ObjectCreated:*"], "lambda_function_arn": aws_lambda.arn}
    ],
)
