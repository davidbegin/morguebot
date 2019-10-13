import pulumi
import json
from modules.s3 import bucket
from pulumi_aws import iam, lambda_
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY

config = pulumi.Config()


s3_lambda_role = iam.Role(
    "god-bot-lambda-role", assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY)
)


# bucket_policy = Output.all(s3_bucket.arn, role_arns).apply(
#     lambda args: json.dumps(
#         {
#             "Version": "2012-10-17",
#             "Id": "MorgueFileBucketPolicy",
#             "Statement": [
#                 {
#                     "Sid": "Allow",
#                     "Effect": "Allow",
#                     "Principal": {"AWS": args[1]},
#                     "Action": "s3:*",
#                     "Resource": f"{args[0]}/*",
#                 }
#             ],
#         }
#     )
# )


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
                },
                {"Effect": "Allow", "Action": ["s3:PutObject"], "Resource": bucket_arn},
                {
                    "Effect": "Allow",
                    "Action": ["sqs:*"],
                    "Resource": "arn:aws:sqs:us-west-2:851075464416:new-gods-queue-6fecb43",
                },
                {
                    "Effect": "Allow",
                    "Action": ["kinesis:PutRecord"],
                    "Resource": "arn:aws:kinesis:us-west-2:851075464416:stream/twitch-chat-877759c",
                },
            ],
        }
    )


# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy(
    "god-bot-lambda-role-policy",
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
    "god-bot",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="god_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)
