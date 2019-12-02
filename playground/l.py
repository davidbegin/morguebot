import json

import boto3

client = boto3.client("lambda")

response = client.invoke(
    FunctionName="destinations-lambda-a2f8fc7",
    InvocationType="Event",
    Payload=json.dumps({"succfsfess": False})
)


print(response)
