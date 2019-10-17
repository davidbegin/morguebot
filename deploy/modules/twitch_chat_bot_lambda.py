import pulumi
import json
from pulumi import Output
from modules.s3 import bucket
from modules.kinesis import chat_stream
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import kms, iam, lambda_
from modules.dynamodb import dynamodb_table

config = pulumi.Config()

kms_key = kms.Key("twitch-chat-bot")

module_name = "twitch-chat-bot"

twitch_oauth_token = kms.Ciphertext(
    "twitch_oauth_token,",
    key_id=kms_key.arn,
    plaintext=config.require_secret("oauth_token"),
)

s3_lambda_role = iam.Role(
    f"{module_name}-role", assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY)
)

lambda_role_policy = Output.all(bucket.arn, chat_stream.arn, kms_key.arn).apply(
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

# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy(
    f"{module_name}-role-policy", role=s3_lambda_role.id, policy=lambda_role_policy
)

iam.RolePolicyAttachment(
    f"{module_name}-xray",
    policy_arn = "arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role = s3_lambda_role.id
)

# source_code_hash=None
# https://morgue-artifacts.s3-us-west-2.amazonaws.com/handler.zip
# TODO: Add the source_hash_code thang to trigger updates
cloudwatch_lambda = lambda_.Function(
    f"{module_name}",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="twitch_chat_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    tracing_config={"mode": "Active"},
    timeout=200,
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
    f"{module_name}-kinesis-esm",
    event_source_arn=chat_stream.arn,
    function_name=cloudwatch_lambda.name,
    starting_position="LATEST",
    # starting_position="AT_TIMESTAMP",
    # starting_position_timestamp="AT_TIMESTAMP",
)

# def __init__(batch_size=None, enabled=None,
#         starting_position=None, starting_position_timestamp=None, __props__=None, __name__=None, __opts__=None):
