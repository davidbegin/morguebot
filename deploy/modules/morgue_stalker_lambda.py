import pulumi
import json
from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import iam, lambda_

config = pulumi.Config()

module_name = "morgue-stalker"

s3_lambda_role = iam.Role(
    f"{module_name}-role", assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY)
)


def lambda_role_policy(bucket_arn):
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                CREATE_CW_LOGS_POLICY,
                {
                    "Effect": "Allow",
                    "Action": ["s3:PutObject", "s3:ListObjectsV2"],
                    "Resource": bucket_arn,
                },
                {
                    "Effect": "Allow",
                    "Action": ["s3:GetObject"],
                    "Resource": f"{bucket_arn}/*",
                },
            ],
        }
    )


# TODO: comeback and fix this string interpolation
lambda_role_policy = iam.RolePolicy(
    f"{module_name}-role-policy",
    role=s3_lambda_role.id,
    policy=bucket.arn.apply(lambda_role_policy),
)

iam.RolePolicyAttachment(
    f"{module_name}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=s3_lambda_role.id,
)


# source_code_hash=None
# https://morgue-artifacts.s3-us-west-2.amazonaws.com/handler.zip
# TODO: Add the source_hash_code thang to trigger updates
cloudwatch_lambda = lambda_.Function(
    f"{module_name}",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="morgue_stalker.chandler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    tracing_config={"mode": "Active"},
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)

lambda_.Permission(
    "AllowInvocationFromCloudWatch",
    action="lambda:InvokeFunction",
    function=cloudwatch_lambda.arn,
    principal="events.amazonaws.com",
)
