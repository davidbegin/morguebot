from pulumi_aws import sns, iam
import json

sqs_arn = "arn:aws:sqs:us-west-2:851075464416:new-gods-queue-6fecb43"
god_queue_topic_role = iam.Role(
    "god-queue-topic-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "sns.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }""",
)

policy = json.dumps(
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

lambda_role_policy = iam.RolePolicy(
    "god-bot-topic-lambda-policy", role=god_queue_topic_role.id, policy=policy
)

# sns_topic = sns.Topic("god-queue-topic", sqs_success_feedback_role_arn=god_queue_topic_role.arn)
sns_topic = sns.Topic(
    "god-queue-topic",
    sqs_failure_feedback_role_arn=god_queue_topic_role.arn,
    sqs_success_feedback_role_arn=god_queue_topic_role.arn,
)

# class pulumi_aws.sns.Topic(resource_name, opts=None, application_failure_feedback_role_arn=None, application_success_feedback_role_arn=None, application_success_feedback_sample_rate=None, delivery_policy=None, display_name=None, http_failure_feedback_role_arn=None, http_success_feedback_role_arn=None, http_success_feedback_sample_rate=None, kms_master_key_id=None, lambda_failure_feedback_role_arn=None, lambda_success_feedback_role_arn=None, lambda_success_feedback_sample_rate=None, name=None, name_prefix=None, policy=None, sqs_failure_feedback_role_arn=None, sqs_success_feedback_role_arn=None, sqs_success_feedback_sample_rate=None, tags=None, __props__=None, __name__=None, __opts__=None)
