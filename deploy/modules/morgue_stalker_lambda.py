import pulumi
import json
from modules.s3 import bucket
from modules.iam import LAMBDA_ASSUME_ROLE_POLICY
from modules.iam import CREATE_CW_LOGS_POLICY
from pulumi_aws import iam, lambda_
from pulumi_aws import cloudwatch

config = pulumi.Config()

MODULE_NAME = "morgue-stalker"

role = iam.Role(
    f"{MODULE_NAME}-role", assume_role_policy=json.dumps(LAMBDA_ASSUME_ROLE_POLICY)
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


iam.RolePolicy(
    f"{MODULE_NAME}-role-policy",
    role=role.id,
    policy=bucket.arn.apply(lambda_role_policy),
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
    handler="lambda_handler.morgue_stalker",
    s3_key=config.require("artifact_name"),
    s3_bucket="morgue-artifacts",
    tracing_config={"mode": "Active"},
    timeout=900,
    environment={"variables": {"MORGUE_BUCKETNAME": bucket.id}},
)

event_rule = cloudwatch.EventRule(
    f"{MODULE_NAME}-event-rule",
    name=f"{MODULE_NAME}-very-cool-every-minute",
    schedule_expression="rate(1 minute)",
)

event_target = cloudwatch.EventTarget(
    f"{MODULE_NAME}-event-target", arn=aws_lambda.arn, rule=event_rule.name
)

lambda_.Permission(
    "AllowInvocationFromCloudWatch",
    action="lambda:InvokeFunction",
    function=aws_lambda.arn,
    principal="events.amazonaws.com",
    source_arn=event_rule.arn,
)
