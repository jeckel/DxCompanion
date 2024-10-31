from typing import Optional

from textual import on
from textual.widgets import Button

from .composer_message import ComposerCommandRequested


class ComposerScriptButton(Button):
    """
    Button to launch a composer script
    """

    def __init__(
        self,
        script: str,
        label: Optional[str] = None,
        allow_rerun: bool = False,
        refresh_composer_on_success: bool = False,
        **kwargs,
    ):
        self.script = script
        self.allow_rerun = allow_rerun
        self.refresh_composer_on_success = refresh_composer_on_success
        super().__init__(label or script, id=f"composer-button-{script}", **kwargs)

    @on(Button.Pressed)
    def on_pressed(self, event: Button.Pressed) -> None:
        self.post_message(
            ComposerCommandRequested(
                script=self.script,
                allow_rerun=self.allow_rerun,
                refresh_composer_on_success=self.refresh_composer_on_success,
            )
        )
