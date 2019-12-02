import pulumi

import json
from pulumi import Output
from pulumi_aws import lambda_

from modules.dynamodb import dynamodb_table
from modules.sqs import gods_queue
from modules.sqs import errors_queue
from modules.kinesis import chat_stream
from modules.kinesis import error_stream
from modules.s3 import bucket
from modules.sns import sns_topic
from modules.sns import weapons_topic

import modules.morgue_bot_lambda
import modules.morgue_stalker_lambda
import modules.twitch_chat_bot_lambda
import modules.weapons_bot_lambda
import modules.god_bot_lambda
import modules.xl_bot_lambda

pulumi.export("sqs_queue", gods_queue.name)
pulumi.export("errors_sqs_queue", errors_queue.name)
pulumi.export("errors_sqs_queue_arn", errors_queue.arn)
pulumi.export("errors_stream_arn", error_stream.arn)


pulumi.export("weapons_bot_lambda", modules.weapons_bot_lambda.aws_lambda.name)
pulumi.export("xl_bot_lambda", modules.xl_bot_lambda.aws_lambda.name)

pulumi.export("dyanmodb_table", dynamodb_table.name)
pulumi.export("dyanmodb_stream_arn", dynamodb_table.stream_arn)
pulumi.export("kinesis_arn", chat_stream.arn)
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
pulumi.export("sns_topic_arn", sns_topic.arn)
pulumi.export("weapons_topic_arn", weapons_topic.arn)

pulumi.export("morgue_stalker_lambda", modules.morgue_stalker_lambda.aws_lambda.name),
pulumi.export("morguebot_lambda", modules.morgue_bot_lambda.aws_lambda.name),
pulumi.export("god_bot_lambda", modules.god_bot_lambda.aws_lambda.name),
pulumi.export("twitch_chat_bot_lambda", modules.twitch_chat_bot_lambda.aws_lambda.name)
pulumi.export("dungeon_gossiper_lambda", modules.dungeon_gossiper.aws_lambda.name)

lambda_arn = "arn:aws:lambda:us-west-2:851075464416:function:lambda-authorizer"
authorizer_lambda = lambda_.GetFunctionResult(arn=lambda_arn)
# pulumi.export("zzzz____authorizer_lambda", type(authorizer_lambda))
# pulumi.export("yyy____authorizer_lambda", "A Test")

# pulumi.export(
#     "lambda_env_vars",
#     {
#         "god_bot": modules.god_bot_lambda.lambda_variables,
#         "morgue_bot": modules.morgue_bot_lambda.lambda_variables,
#     },
# )

# pulumi.export(
#     "cloudwatch_logs",
#     [
#         Output.concat("/aws/lambda/", modules.morgue_stalker_lambda.aws_lambda.name),
#         Output.concat("/aws/lambda/", modules.morgue_bot_lambda.aws_lambda.name),
#         Output.concat("/aws/lambda/", modules.god_bot_lambda.aws_lambda.name),
#         Output.concat("/aws/lambda/", modules.twitch_chat_bot_lambda.aws_lambda.name),
#     ],
# )

# Export the Lambda environment variables to a file!
