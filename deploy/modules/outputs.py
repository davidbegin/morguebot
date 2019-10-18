import pulumi

from modules.sqs import gods_queue

pulumi.export("sqs_queue", gods_queue.name)
