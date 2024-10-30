from typing import Optional

from textual.widgets import Button


class ComposerScriptButton(Button):
    """
    Button to launch a composer script defined in the composer.json file
    """

    def __init__(self, script_name: str, label: Optional[str] = None, **kwargs):
        self.script_name = script_name
        super().__init__(
            label or script_name, id=f"composer-button-{script_name}", **kwargs
        )
