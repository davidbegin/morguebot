import pulumi
from pulumi import Output
import json
from modules.sqs import xl_upgrades_queue
from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import iam, lambda_

from modules.kinesis import chat_stream
from modules.dynamodb import dynamodb_table
from modules.layers import dependency_layer

from modules.sns import sns_topic


config = pulumi.Config()

MODULE_NAME = "xl-bot"

role = iam.Role(
    f"{MODULE_NAME}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

policy = Output.all(
    bucket.arn, xl_upgrades_queue.arn, chat_stream.arn, sns_topic.arn
).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Id": f"{MODULE_NAME}-policy",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {"Effect": "Allow", "Action": ["s3:*"], "Resource": args[0]},
                {"Effect": "Allow", "Action": ["s3:*"], "Resource": f"{args[0]}/*"},
                {"Effect": "Allow", "Action": ["sqs:*"], "Resource": args[1]},
                {
                    "Effect": "Allow",
                    "Action": ["kinesis:PutRecord"],
                    "Resource": args[2],
                },
                {"Effect": "Allow", "Action": ["sns:*"], "Resource": args[3]},
            ],
        }
    )
)

iam.RolePolicy(f"{MODULE_NAME}-lambda-policy", role=role.id, policy=policy)

iam.RolePolicyAttachment(
    f"{MODULE_NAME}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=role.id,
)

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
    handler="handler.lambda_handler",
    s3_key=config.require("artifact_name"),
    tracing_config={"mode": "Active"},
    s3_bucket="morgue-artifacts",
    timeout=200,
    layers=[dependency_layer.arn],
    environment={"variables": lambda_variables},
)

# lambda_.EventSourceMapping(
#     f"{MODULE_NAME}-sqs-esm",
#     event_source_arn=xl_upgrades_queue.arn,
#     function_name=aws_lambda.name,
# )

lambda_.Permission(
    "AllowInvocationFromSQSQueue",
    action="lambda:InvokeFunction",
    function=aws_lambda.arn,
    principal="sqs.amazonaws.com",
    source_arn=xl_upgrades_queue.arn,
)
