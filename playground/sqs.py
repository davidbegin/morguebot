import boto3


def send_to_gods_queue():
    client = boto3.client("sqs")

    # queue_url = (
    #     "https://sqs.us-west-2.amazonaws.com/851075464416/xl-upgrades-queue-d73d0c6"
    # )
    queue_url = (
        "https://sqs.us-west-2.amazonaws.com/851075464416/errors-queue-4e335cd"
        # "https://sqs.us-west-2.amazonaws.com/851075464416/weapons-queue-4de181e"
    )
    response = client.send_message(
        QueueUrl=queue_url, MessageBody="SEE I CAN DO WHATEVER I WANT"
    )
    print(response)


send_to_gods_queue()
