from textual.app import ComposeResult
from textual.containers import Container
from rich.text import Text
from textual.widgets import DataTable, Button


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

class ComposerScripts(Container):
    BORDER_TITLE = "Composer Scripts"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Button('cs-fix')
        yield Button('analize')