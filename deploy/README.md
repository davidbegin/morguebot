# Architecture

An Example of an event drive architecture using:
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [SQS](https://aws.amazon.com/sqs/)
- [SNS](https://aws.amazon.com/sns/)
- [S3](https://aws.amazon.com/s3/)
- [Kinesis](https://aws.amazon.com/kinesis/)
- [DynamoDB](https://aws.amazon.com/dynamodb/)
- [X-Ray](https://aws.amazon.com/xray/)

![Morguebot](../images/MorgueArch.png)

### Morgue Parser

A simple Lambda that is monitoring for new Morgue Files, and once they find one, saving it to S3.

Permissions:
  - Put Objects from the Morgue Files S3 Bucket

### Morgue Bot

The Main Brain of our system.
Responds to New Objects (in this case morgue files) dropped into an S3 Bucket. When a new object is dropped, it parses it and updates the Main Datastore DynamoDB, it then sends off SNS messages about all the categories that changed.

Permissions:
  - Get Objects from the Morgue Files S3 Bucket
  - Get and Put Objects into DynamoDB
  - Permission to Send off SNS Messsages

### Gods Bot

A Lambda with a SQS Event Source, that will take a message about new Gods and then calculate a message to send. Which it will invoke the twitch bit to send to the Chat.

Permissions:
  - Receive SQS Messages
  - Invoke the Twitch Chat Bot


### XL Bot

A Lambda with a SQS Event Source, that will take a message about Experiece Level Upgrades and then calculate a message to send. Which it will invoke the twitch bit to send to the Chat.

Permissions:
  - Receive SQS Messages
  - Right to the Chat Bot Kinesis Stream

### Twitch Chat Bot

Kinesis Stream Event source Lambda whose sole responsiblility is talking to Twitch.

Permissions:
  - Permission to Read off the Kinesis Stream
  - Ouath Permissions to talk to Twitch
