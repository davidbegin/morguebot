import pulumi
import json
from modules.s3 import bucket
from pulumi_aws import iam, lambda_

config = pulumi.Config()


s3_lambda_role = iam.Role(
    "xl-bot-lambda-role",
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
    "xl-bot-lambda-policy",
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
    "xl-bot",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="xl_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)
