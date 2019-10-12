import pulumi
from pulumi import Output
import json
from pulumi_aws import s3, lambda_, iam

config = pulumi.Config()

print(config.require_secret("oauth_token"))

# ============
# IAM
# ============

lambda_role = iam.Role(
    "lambdaRole",
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


# ============
# S3
# ============

bucket = s3.Bucket("morgue-files")
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)

bucket_arn = bucket.arn
lambda_role_arn = lambda_role.arn

# ========================================================================================

kms_key_arn = "arn:aws:kms:us-west-2:851075464416:key/6d11ced0-ca8c-4057-bc61-4fd8d27da705"


policy = Output.all(lambda_role.arn, bucket.arn, kms_key_arn).apply(
    lambda args: json.dumps(
        {
            "Version": "2012-10-17",
            "Id": "MorgueFileBucketPolicy",
            "Statement": [
                {
                    "Sid": "Allow",
                    "Effect": "Allow",
                    "Principal": {"AWS": [args[0]]},
                    "Action": "s3:*",
                    "Resource": f"{args[1]}/*",
                }
                # {
                #     "Sid": "DecryptOauth",
                #     "Effect": "Allow",
                #     "Principal": {"AWS": [args[0]]},
                #     "Action": "kms:*",
                #     "Resource": args[2],
                # },
            ],
        }
    )
)

s3.BucketPolicy("morgue-file-bucket-policy", bucket=bucket.id, policy=policy)

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
            ],
        }
    )


# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy(
    "lambdaRolePolicy", role=lambda_role.id, policy=bucket_arn.apply(lambda_role_policy)
)

# ============
# Lambda
# ============


# source_code_hash=None
# https://morgue-artifacts.s3-us-west-2.amazonaws.com/handler.zip

# TODO: Add the source_hash_code thang to trigger updates
morgue_save_lambda = lambda_.Function(
    "morgue-saver",
    role=lambda_role.arn,
    runtime="python3.6",
    handler="lambda_handler.save_morgue",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)




# ========================================================================================
# MORGUE PARSER
# ========================================================================================

morgue_parser_lambda_role = iam.Role(
    "morgue-parser-lambda-role",
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


# Give this DynamoDB Permissions
# Create DynamoDB Table


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
                {"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": bucket_arn},
                {"Effect": "Allow", "Action": ["dynamodb:GetItem"], "Resource": "arn:aws:dynamodb:us-west-2:851075464416:table/morguebot"},
            ],
        }
    )


morgue_parser_lambda_role_policy = iam.RolePolicy(
    "morgue-parser-lambda-role-policy", role=morgue_parser_lambda_role.id, policy=bucket_arn.apply(morgue_parser_lambda_role_policy)
)


# TODO: Add the source_hash_code thang to trigger updates
morgue_parser_lambda = lambda_.Function(
    "morgue-parser",
    role=morgue_parser_lambda_role.arn,
    runtime="python3.6",
    handler="lambda_handler.status",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)

# How do we get triggered on S3???
