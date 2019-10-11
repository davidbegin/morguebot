import pulumi
from pulumi_aws import s3, lambda_, iam

# ============
# S3
# ============

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('morgue-files')


# Export the name of the bucket
pulumi.export('bucket_name',  bucket.id)
morgue_file_bucket_policy = """{
    "Version": "2012-10-17",
    "Id": "MYBUCKETPOLICY",
    "Statement": [
        {
            "Sid": "Allow",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::851075464416:role/lambda_exec_role",
                    "arn:aws:iam::851075464416:role/lambdaRole-e999bda"
                ]
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::morgue-files-2944dfb/*"
        }
    ]
}
"""
s3.BucketPolicy("morgue-file-bucket-policy", bucket=bucket.id, policy=morgue_file_bucket_policy)

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


# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy('lambdaRolePolicy',
    role=lambda_role.id,
    policy="""{
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
            "Resource": "arn:aws:s3:::morgue-files-2944dfb"
          }
        ]
    }"""
)

# ===== bucket.id

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

