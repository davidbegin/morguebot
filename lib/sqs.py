import boto3


def send_to_gods_queue():
    client = boto3.client("sqs")

    # queue_url = (
    #     "https://sqs.us-west-2.amazonaws.com/851075464416/xl-upgrades-queue-d73d0c6"
    # )
    queue_url = (
        "https://sqs.us-west-2.amazonaws.com/851075464416/new-gods-queue-6fecb43"
    )
    response = client.send_message(QueueUrl=queue_url, MessageBody="Debugging Time")
    print(response)


send_to_gods_queue()
