from lib.morgue_event import MorgueEvent


class TwitchChatParser:
    def __init__(self, chat_msg):
        self.chat_msg = chat_msg

        self._split_msg = chat_msg.split()

        self.command = self._split_msg[0]

        if len(self._split_msg) > 1:
            self.character = self._split_msg[1]
        else:
            self.character = None

        if len(self._split_msg) > 2:
            self.args = self._split_msg[2:]
        else:
            self.args = []

    def parse(self):
        return MorgueEvent(
            command=self.command, character=self.character, args=self.args
        )
