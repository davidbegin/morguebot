from pulumi_aws import sqs

gods_queue = sqs.Queue("new-gods-queue", visibility_timeout_seconds=200)
xl_upgrades_queue = sqs.Queue("xl-upgrades-queue", visibility_timeout_seconds=200)
