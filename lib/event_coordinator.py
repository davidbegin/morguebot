import os
import json
import boto3

from lib.morgue_event_router import MorgueEventRouter


# this invokes a Lambda
class EventCoordinator:
    def __init__(self, morgue_event):
        self.morgue_event = morgue_event
        dest_lambda = MorgueEventRouter(morgue_event).dest_lambda()

        # TODO: We need to pull this in from Pulumi
        if dest_lambda == "dungeon_gossiper":
            self.lambda_target = "dungeon-gossiper-e3a74e7"
        else:
            self.lambda_target = "morgue-stalker-f15d681"

        # There is a delegate pattern for this
        self.character = morgue_event.character
        self.command = morgue_event.command
        self.arguments = morgue_event.args
        self.search = morgue_event.search
        self.level_barrier = morgue_event.level_barrier
        self.lambda_client = boto3.client("lambda")

    # review the commands the decide what to do
    # evaluate any special flags, that run this in a different mode: AKA Local
    def coordinate(self):
        self._description()
        return self.invoke_lambda()

    def invoke_lambda(self):
        payload = {
            "character": self.character,
            "command": self.command,
            "search": self.search,
            "level": self.level_barrier,
        }

        if "TEST_MODE" in os.environ:
            print(
                "\033[36mWE are in Test Mode, this is no time to invoke Lambdas\033[0m"
            )
            return
        else:
            return self.lambda_client.invoke(
                FunctionName=self.lambda_target, Payload=json.dumps(payload)
            )

    def _description(self):
        print(
            f"\033[33mInvoking {self.lambda_target}\033[0m \033[037;1mcharacter:\033[0m \033[36m{self.character}\033[0m \033[37;1mcommand:\033[0m \033[36m{self.command}\033[0m \033[37;1margs:\033[0m \033[36m{self.arguments}\033[0m"
        )
