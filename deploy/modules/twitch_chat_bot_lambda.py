import pulumi
import json
from modules.s3 import bucket
from pulumi_aws import kms, iam, lambda_

config = pulumi.Config()

pulumi.log.info(f"{config.require_secret('oauth_token')}")

key_id = "arn:aws:kms:us-west-2:851075464416:key/6d11ced0-ca8c-4057-bc61-4fd8d27da705"
twitch_oauth_token = kms.Ciphertext(
    "twitch_oauth_token,", key_id=key_id, plaintext=config.require_secret("oauth_token")
)

s3_lambda_role = iam.Role(
    "twitch-chat-bot-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }""",
)


def lambda_role_policy(bucket_arn):
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    "Resource": "arn:aws:logs:*:*:*",
                }
            ],
        }
    )


# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy(
    "twitch-chat-bot-role-policy",
    role=s3_lambda_role.id,
    policy=bucket.arn.apply(lambda_role_policy),
)

# ============
# Lambda
# ============


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
            "TWITCH_OAUTH_TOKEN": twitch_oauth_token.ciphertext_blob,
        }
    },
)
