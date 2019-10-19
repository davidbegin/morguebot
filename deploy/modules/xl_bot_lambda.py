import pulumi
import json
from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import iam, lambda_

config = pulumi.Config()

MODULE_NAME = "xl-bot"

role = iam.Role(
    f"{MODULE_NAME}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)


def policy(bucket_arn):
    return json.dumps({"Version": "2012-10-17", "Statement": [CREATE_CW_LOGS_POLICY]})


iam.RolePolicy(
    f"{MODULE_NAME}-lambda-policy", role=role.id, policy=bucket.arn.apply(policy)
)

iam.RolePolicyAttachment(
    f"{MODULE_NAME}-xray",
    policy_arn="arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess",
    role=role.id,
)

aws_lambda = lambda_.Function(
    f"{MODULE_NAME}",
    role=role.arn,
    runtime="python3.6",
    handler="lambda_handler.xl_bot",
    s3_key=config.require("artifact_name"),
    tracing_config={"mode": "Active"},
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)
