import pulumi

from modules.dynamodb import dynamodb_table
from modules.sqs import gods_queue
from modules.kinesis import chat_stream
from modules.s3 import bucket
from modules.sns import sns_topic

import modules.morgue_bot_lambda
import modules.morgue_stalker_lambda
import modules.twitch_chat_bot_lambda
import modules.weapons_bot_lambda
import modules.xl_bot_lambda

pulumi.export("sqs_queue", gods_queue.name)
pulumi.export("morguebot_lambda", modules.morgue_bot_lambda.aws_lambda.name)
pulumi.export("morgue_stalker_lambda", modules.morgue_stalker_lambda.aws_lambda.name)
pulumi.export("twitch_chat_bot_lambda", modules.twitch_chat_bot_lambda.aws_lambda.name)
pulumi.export("weapons_bot_lambda", modules.weapons_bot_lambda.aws_lambda.name)
pulumi.export("xl_bot_lambda", modules.xl_bot_lambda.aws_lambda.name)
pulumi.export("dyanmodb_table", dynamodb_table.name)
pulumi.export("kinesis_arn", chat_stream.arn)
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
pulumi.export("sns_topic_arn", sns_topic.arn)
