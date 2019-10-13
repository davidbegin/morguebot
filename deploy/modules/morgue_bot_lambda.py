from modules.s3 import bucket

import json

from pulumi_aws import iam, lambda_
import pulumi

config = pulumi.Config()

# ========================================================================================
# MORGUE PARSER
# ========================================================================================
morgue_parser_lambda_role = iam.Role(
    "morgue-bot-lambda-role",
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


def morgue_parser_lambda_role_policy(bucket_arn):
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
                {"Effect": "Allow", "Action": ["s3:*"], "Resource": bucket_arn},
                {
                    "Effect": "Allow",
                    "Action": ["sns:Publish"],
                    "Resource": "arn:aws:sns:us-west-2:851075464416:god-queue-topic-a3644eb",
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                    ],
                    "Resource": "arn:aws:dynamodb:us-west-2:851075464416:table/morguebot",
                },
            ],
        }
    )


# How do we hook this up to an S3 Object Notifcation

morgue_parser_lambda_role_policy = iam.RolePolicy(
    "morgue-bot-lambda-role-policy",
    role=morgue_parser_lambda_role.id,
    policy=bucket.arn.apply(morgue_parser_lambda_role_policy),
)


# TODO: Add the source_hash_code thang to trigger updates
morgue_parser_lambda = lambda_.Function(
    "morgue-bot",
    role=morgue_parser_lambda_role.arn,
    runtime="python3.6",
    handler="morgue_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)

# class pulumi_aws.lambda_.Permission(resource_name, opts=None, action=None, event_source_token=None, function=None, principal=None, qualifier=None, source_account=None, source_arn=None, statement_id=None, statement_id_prefix=None, __props__=None, __name__=None, __opts__=None

lambda_.Permission(
    "AllowInvocationFromMorgueFileBucket",
    action="lambda:InvokeFunction",
    function=morgue_parser_lambda.arn,
    principal="s3.amazonaws.com",
    source_arn="arn:aws:s3:::morgue-files-2944dfb",
)
