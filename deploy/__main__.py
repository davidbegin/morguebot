import json

import pulumi
from pulumi import Output
from pulumi_aws import s3, lambda_, iam

from modules.dynamodb import dynamodb_table

from modules.s3 import bucket

from modules.s3_lambda import morgue_parser_lambda_role
from modules.s3_lambda import morgue_parser_lambda

from modules.cloudwatch_lambda import cloudwatch_lambda

from modules.s3 import allow_s3_bucket_access

allow_s3_bucket_access(bucket, [morgue_parser_lambda_role])
