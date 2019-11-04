from lib.morgue_event import MorgueEvent


class CommandLineParser:
    @classmethod
    def from_options(cls, options):
        command = options.command
        character = options.character
        level_barrier = options.level_barrier
        search = options.search

        # return MorgueEvent(
        # )
