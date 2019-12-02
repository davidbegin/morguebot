import pulumi
from pulumi import Output
import json
from modules.kinesis import chat_stream
from modules.sqs import weapons_queue
from pulumi_aws import iam, lambda_, sns
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from modules.sns import weapons_topic
from modules.layers import dependency_layer


config = pulumi.Config()

MODULE_NAME = "weapons-bot"

role = iam.Role(
    f"{MODULE_NAME}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)

policy = Output.all(weapons_queue.arn, chat_stream.arn).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Id": f"{MODULE_NAME}-policy",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {"Effect": "Allow", "Action": ["sqs:*"], "Resource": args[0]},
                {
                    "Effect": "Allow",
                    "Action": ["kinesis:PutRecord"],
                    "Resource": args[1],
                },
            ],
        }
    )
)


iam.RolePolicy(f"{MODULE_NAME}-lambda-role-policy", role=role.id, policy=policy)

iam.RolePolicyAttachment(
    f"{MODULE_NAME}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=role.id,
)

aws_lambda = lambda_.Function(
    f"{MODULE_NAME}",
    role=role.arn,
    runtime="python3.6",
    handler="lambda_handler.weapons_bot",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    tracing_config={"mode": "Active"},
    timeout=200,
    layers=[dependency_layer.arn],
    environment={
        "variables": {
            "CHAT_STREAM_ARN": chat_stream.arn,
            "CHAT_STREAM_NAME": chat_stream.name,
        }
    },
)

# lambda_.EventSourceMapping(
#     f"{MODULE_NAME}-sqs-esm",
#     event_source_arn=weapons_queue.arn,
#     function_name=aws_lambda.name,
# )
