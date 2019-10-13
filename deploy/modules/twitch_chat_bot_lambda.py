import pulumi
import json
from pulumi import Output
from modules.s3 import bucket
from modules.kinesis import chat_stream
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import kms, iam, lambda_

config = pulumi.Config()

key_id = "arn:aws:kms:us-west-2:851075464416:key/6d11ced0-ca8c-4057-bc61-4fd8d27da705"
twitch_oauth_token = kms.Ciphertext(
    "twitch_oauth_token,", key_id=key_id, plaintext=config.require_secret("oauth_token")
)

s3_lambda_role = iam.Role(
    "twitch-chat-bot-role", assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY)
)

kms_key_arn = (
    "arn:aws:kms:us-west-2:851075464416:key/6d11ced0-ca8c-4057-bc61-4fd8d27da705"
)

lambda_role_policy = Output.all(bucket.arn, chat_stream.arn).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {
                    "Sid": "AllowKms",
                    "Effect": "Allow",
                    "Action": "kms:Decrypt",
                    "Resource": kms_key_arn,
                },
                {
                    "Sid": "AllowKinesis",
                    "Effect": "Allow",
                    "Action": "kinesis:*",
                    "Resource": f"{args[1]}",
                },
                {
                    "Sid": "AllowS3",
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": f"{args[0]}/*",
                },
            ],
        }
    )
)

# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy(
    "twitch-chat-bot-role-policy", role=s3_lambda_role.id, policy=lambda_role_policy
)

# source_code_hash=None
# https://morgue-artifacts.s3-us-west-2.amazonaws.com/handler.zip
# TODO: Add the source_hash_code thang to trigger updates
cloudwatch_lambda = lambda_.Function(
    "twitch-chat-bot",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="twitch_chat_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={
        "variables": {
            "MORGUE_BUCKETNAME": bucket.id,
            "MORGUEBOT_TWITCH_OAUTH_TOKEN": twitch_oauth_token.ciphertext_blob,
            "MORGUEBOT_BOT_NAME": "beginbotbot",
            "MORGUEBOT_CHANNEL": "beginbot",
        }
    },
)
