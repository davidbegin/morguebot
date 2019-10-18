import json

import pulumi
from pulumi import Output
from pulumi_aws import s3, lambda_, iam

from modules.dynamodb import dynamodb_table

from modules.s3 import bucket

from modules.morgue_bot_lambda import morgue_parser_lambda_role
from modules.morgue_bot_lambda import morgue_parser_lambda

from modules.morgue_stalker_lambda import cloudwatch_lambda
from modules.morgue_stalker_lambda import s3_lambda_role

from modules.s3 import allow_s3_bucket_access


import modules.xl_bot_lambda
import modules.god_bot_lambda
import modules.weapons_bot_lambda
import modules.morgue_stalker_lambda
import modules.twitch_chat_bot_lambda

import modules.kinesis

import modules.sqs
import modules.sns

allow_s3_bucket_access(
    bucket, [morgue_parser_lambda_role, s3_lambda_role], morgue_parser_lambda
)


import modules.outputs
