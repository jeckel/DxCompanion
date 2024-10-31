from textual.message import Message

from .terminal import CommandType


class TerminalCommandRequested(Message):
    def __init__(
        self,
        command: CommandType,
        allow_rerun: bool = True,
    ):
        self.command = command
        self.allow_rerun = allow_rerun
        super().__init__()
