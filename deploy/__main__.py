import pulumi
from pulumi import Output
import json
from pulumi_aws import s3, lambda_, iam

# ============
# IAM
# ============

lambda_role = iam.Role('lambdaRole',
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
    }"""
)


# ============
# S3
# ============

bucket = s3.Bucket('morgue-files')
pulumi.export('bucket_name',  bucket.id)
pulumi.export('bucket_arn',  bucket.arn)

bucket_arn = bucket.arn
lambda_role_arn = lambda_role.arn

def morgue_file_bucket_policy(bucket_arn, lambda_role_arn):
    return json.dumps({
        "Version": "2012-10-17",
        "Id": "MYBUCKETPOLICY",
        "Statement": [
            {
                "Sid": "Allow",
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        lambda_role_arn
                        ]
                    },
                "Action": "s3:*",
                "Resource": f"{bucket_arn}/*"
                }
            ]
        })


# signed_blob_url = Output.all(storage_account.name, storage_container.name, blob.name, account_sas.sas) \
#     .apply(lambda args: f"https://{args[0]}.blob.core.windows.net/{args[1]}/{args[2]}{args[3]}")

policy = Output.all(lambda_role.arn, bucket.arn) \
        .apply(lambda args: json.dumps({
            "Version": "2012-10-17",
            "Id": "MYBUCKETPOLICY",
            "Statement": [
                {
                    "Sid": "Allow",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            args[0]
                            ]
                        },
                    "Action": "s3:*",
                    "Resource": f"{args[1]}/*"
                    }
                ]
            })
            )

s3.BucketPolicy(
    "morgue-file-bucket-policy",
    bucket=bucket.id,
    policy=policy
)


def lambda_role_policy(bucket_arn):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
          },
          {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": bucket_arn
          }
        ]
    })


# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy('lambdaRolePolicy',
    role=lambda_role.id,
    policy=bucket_arn.apply(lambda_role_policy)
)

# ============
# Lambda
# ============

# WE need to create out Lambda and set the bucket ID as env environment variable

# TODO: Add the source_hash_code thang to trigger updates
hello_world_fn = lambda_.Function('morgue-saver',
    role=lambda_role.arn,
    runtime="python3.6",
    handler="lambda_handler.save_morgue",
    code="../build/handler2.zip",
    timeout=200,
    environment={
        "variables": {
            "MORGUE_BUCKETNAME": bucket.id
        }
    }
)
