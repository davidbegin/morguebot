import json
import pulumi
from pulumi_aws import s3
from pulumi import Output

# ============
# S3
# ============

bucket = s3.Bucket("morgue-files")
# pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)


def allow_s3_bucket_access(s3_bucket, roles, lamda_function_arn):
    # s3.BucketNotification("new-morgue-file", bucket=s3_bucket.arn, lambda_functions=[lamda_function_arn])

    role_arns = [role.arn for role in roles]

    bucket_policy = Output.all(s3_bucket.arn, role_arns).apply(
        lambda args: json.dumps(
            {
                "Version": "2012-10-17",
                "Id": "MorgueFileBucketPolicy",
                "Statement": [
                    {
                        "Sid": "Allow",
                        "Effect": "Allow",
                        "Principal": {"AWS": args[1]},
                        "Action": "s3:*",
                        "Resource": f"{args[0]}/*",
                    }
                ],
            }
        )
    )

    s3.BucketPolicy(
        "morgue-file-bucket-policy", bucket=s3_bucket.id, policy=bucket_policy
    )
