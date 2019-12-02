import json

from pulumi_aws import apigateway
from pulumi_aws import iam
from pulumi_aws import lambda_

MODULE_NAME = "morguebot"

rest_api = apigateway.RestApi(MODULE_NAME)

resource = apigateway.Resource(
    MODULE_NAME,
    rest_api=rest_api,
    parent_id=rest_api.root_resource_id,
    path_part="dungeon_gossiper",
)

lambda_arn = "arn:aws:lambda:us-west-2:851075464416:function:lambda-authorizer"


def authorizer_role_policy():
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["lambda:InvokeFunction"],
                    "Resource": lambda_arn,
                }
            ],
        }
    )


API_GATEWAY_AUTH_INVOCATION = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {"Service": "apigateway.amazonaws.com"},
            "Effect": "Allow",
            "Sid": "ApigatewayAssumeRole",
        }
    ],
}
role = iam.Role(MODULE_NAME, assume_role_policy=json.dumps(API_GATEWAY_AUTH_INVOCATION))

iam.RolePolicy(
    f"{MODULE_NAME}-role-policy", role=role.id, policy=authorizer_role_policy()
)

# resource "aws_api_gateway_authorizer" "demo" {
#   name                   = "demo"
#   rest_api_id            = "${aws_api_gateway_rest_api.demo.id}"
#   authorizer_uri         = "${aws_lambda_function.authorizer.invoke_arn}"
#   authorizer_credentials = "${aws_iam_role.invocation_role.arn}"
# }


# (Optional, required for type TOKEN/REQUEST) The authorizer's Uniform Resource Identifier (URI).
# This must be a well-formed Lambda function URI in the form of
# arn:aws:apigateway:{region}:lambda:path/{service_api},
# # arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2:012345678912:function:my-function/invocations


# error: Plan apply failed: authorizer_uri must be set non-empty when authorizer type is REQUEST
# Plan apply failed: authorizer_uri must be set non-empty when authorie is TOKEN
authorizer_lambda = lambda_.GetFunctionResult(arn=lambda_arn)

# apigateway.Authorizer(
#     MODULE_NAME,
#     rest_api=rest_api,
#     type="REQUEST",
#     authorizer_uri=authorizer_lambda.invoke_arn,
#     authorizer_credentials=role.arn,
# )


# resource "aws_iam_role" "invocation_role" {
#   name = "api_gateway_auth_invocation"
#   path = "/"

# resource "aws_iam_role_policy" "invocation_policy" {
#   name = "default"
#   role = "${aws_iam_role.invocation_role.id}"

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": "lambda:InvokeFunction",
#       "Effect": "Allow",
#       "Resource": "${aws_lambda_function.authorizer.arn}"
#     }
#   ]
# }
# EOF
# }

meth = apigateway.Method(
    MODULE_NAME,
    rest_api=rest_api,
    resource_id=resource.id,
    http_method="ANY",
    authorization="NONE",
    # authorizer_id=authorizer.id
)
