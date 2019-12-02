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
from modules.layers import dependency_layer

config = pulumi.Config()

MODULE_NAME = "god-bot"

role = iam.Role(
    f"{MODULE_NAME}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

policy = Output.all(bucket.arn, gods_queue.arn, chat_stream.arn).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Id": f"{MODULE_NAME}-policy",
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
    f"{MODULE_NAME}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=role.id,
)

iam.RolePolicy(f"{MODULE_NAME}-lambda-role-policy", role=role.id, policy=policy)

lambda_variables = Output.all(
    dynamodb_table.name, bucket.id, chat_stream.arn, chat_stream.name
).apply(
    lambda args: {
        "CHARACTER_DB": args[0],
        "MORGUE_BUCKETNAME": args[1],
        "CHAT_STREAM_ARN": args[2],
        "CHAT_STREAM_NAME": args[3],
    }
)

aws_lambda = lambda_.Function(
    f"{MODULE_NAME}",
    role=role.arn,
    runtime="python3.6",
    handler="lambda_handler.god_bot",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    tracing_config={"mode": "Active"},
    environment={"variables": lambda_variables},
    layers=[dependency_layer.arn],
)

# lambda_.EventSourceMapping(
#     f"{MODULE_NAME}-sqs-esm",
#     event_source_arn=gods_queue.arn,
#     function_name=aws_lambda.name,
# )
