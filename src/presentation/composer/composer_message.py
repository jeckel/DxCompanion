from textual.message import Message


class ComposerCommandRequested(Message):
    def __init__(
        self,
        script: str | list[str],
        allow_rerun: bool = True,
        refresh_composer_on_success: bool = False,
    ):
        self.script = script
        self.allow_rerun = allow_rerun
        self.refresh_composer_on_success = refresh_composer_on_success
        super().__init__()

    @property
    def command(self) -> list[str]:
        if isinstance(self.script, str):
            return ["composer", "--no-ansi", self.script]
        return ["composer", "--no-ansi", *self.script]
