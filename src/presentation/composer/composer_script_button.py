from textual.widgets import Button


class ComposerScriptButton(Button):
    """
    Button to launch a composer script defined in the composer.json file
    """

    def __init__(self, script_name: str, **kwargs):
        self.script_name = script_name
        super().__init__(script_name, id=f"composer-button-{script_name}", **kwargs)
