import json

import modules.dynamodb
import modules.god_bot_lambda
import modules.kinesis
import modules.morgue_stalker_lambda
import modules.sns
import modules.sqs
import modules.twitch_chat_bot_lambda
import modules.weapons_bot_lambda
import modules.xl_bot_lambda

from modules.s3 import bucket, allow_s3_bucket_access

import modules.morgue_bot_lambda
import modules.morgue_stalker_lambda

allow_s3_bucket_access(
    bucket,
    [modules.morgue_bot_lambda.role, modules.morgue_stalker_lambda.role],
    modules.morgue_bot_lambda.aws_lambda,
)

import modules.outputs
