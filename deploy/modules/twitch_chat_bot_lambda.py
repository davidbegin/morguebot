import pulumi
import json
from pulumi import Output
from modules.s3 import bucket
from modules.kinesis import chat_stream
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import kms, iam, lambda_
from modules.dynamodb import dynamodb_table
from modules.layers import dependency_layer

config = pulumi.Config()

MODULE_NAME = "twitch-chat-bot"

kms_key = kms.Key(f"{MODULE_NAME}")

twitch_oauth_token = kms.Ciphertext(
    "twitch_oauth_token,",
    key_id=kms_key.arn,
    plaintext=config.require_secret("oauth_token"),
)

role = iam.Role(
    f"{MODULE_NAME}-role", assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY)
)

policy = Output.all(bucket.arn, chat_stream.arn, kms_key.arn).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {
                    "Sid": "AllowS3",
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": f"{args[0]}/*",
                },
                {
                    "Sid": "AllowKinesis",
                    "Effect": "Allow",
                    "Action": "kinesis:*",
                    "Resource": f"{args[1]}",
                },
                {
                    "Sid": "AllowKms",
                    "Effect": "Allow",
                    "Action": "kms:Decrypt",
                    "Resource": f"{args[2]}",
                },
            ],
        }
    )
)

iam.RolePolicy(f"{MODULE_NAME}-role-policy", role=role.id, policy=policy)

iam.RolePolicyAttachment(
    f"{MODULE_NAME}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=role.id,
)

aws_lambda = lambda_.Function(
    f"{MODULE_NAME}",
    role=role.arn,
    runtime="python3.6",
    handler="lambda_handler.twitch_chat_bot",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    tracing_config={"mode": "Active"},
    timeout=200,
    layers=[dependency_layer.arn],
    environment={
        "variables": {
            "CHARACTER_DB": dynamodb_table.name,
            "MORGUE_BUCKETNAME": bucket.id,
            "MORGUEBOT_TWITCH_OAUTH_TOKEN": twitch_oauth_token.ciphertext_blob,
            "MORGUEBOT_BOT_NAME": "beginbotbot",
            "MORGUEBOT_CHANNEL": "beginbot",
        }
    },
)

lambda_.EventSourceMapping(
    f"{MODULE_NAME}-kinesis-very-cool-esm",
    event_source_arn=chat_stream.arn,
    function_name=aws_lambda.name,
    starting_position="LATEST",
)
