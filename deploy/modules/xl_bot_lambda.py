import pulumi
import json
from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import iam, lambda_

config = pulumi.Config()

module_name = "xl-bot"

s3_lambda_role = iam.Role(
    f"{module_name}-lambda-role",
    assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY),
)


def lambda_role_policy(bucket_arn):
    return json.dumps({"Version": "2012-10-17", "Statement": [CREATE_CW_LOGS_POLICY]})


lambda_role_policy = iam.RolePolicy(
    f"{module_name}-lambda-policy",
    role=s3_lambda_role.id,
    policy=bucket.arn.apply(lambda_role_policy),
)

# source_code_hash=None
# https://morgue-artifacts.s3-us-west-2.amazonaws.com/handler.zip
# TODO: Add the source_hash_code thang to trigger updates
cloudwatch_lambda = lambda_.Function(
    f"{module_name}",
    role=s3_lambda_role.arn,
    runtime="python3.6",
    handler="xl_bot.handler",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    timeout=200,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)
