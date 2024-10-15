from rich.text import Text
from textual.widgets import DataTable

from models.composer import Package


class ComposerRequireTable(DataTable):
    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.add_columns(*('Package', 'Version'))

    def set_requirements(self, requirements: dict[str, Package]) -> None:
        for package in requirements.values():
            styled_row = (
                Text(str(package.name), justify="left"),
                Text(str(package.version), style="italic #03AC13", justify="right")
            )
            self.add_row(*styled_row)