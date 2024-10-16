from textual.containers import Container, VerticalScroll, Horizontal
from rich.text import Text
from textual.widgets import DataTable, Button, Label, RichLog


class ComposerRequireTable(DataTable):
    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.add_columns(*('Package', 'Version'))

    def set_requirements(self, requirements: dict[str, str]) -> None:
        for package, version in requirements.items():
            styled_row = (
                Text(str(package), justify="left"),
                Text(str(version), style="italic #03AC13", justify="right")
            )
            self.add_row(*styled_row)

class ComposerScriptButton(Button):
    def __init__(self, script_name: str, **kwargs):
        self.script_name = script_name
        super().__init__(script_name, id=f"composer-button-{script_name}", **kwargs)
        self.script_name = script_name

class ComposerScripts(Horizontal):
    BORDER_TITLE = "Composer Scripts"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
