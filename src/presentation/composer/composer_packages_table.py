from rich.text import Text
from textual.widgets import DataTable
from textual import on

from .composer_message import ComposerCommandRequested


class ComposerPackagesTable(DataTable):
    """
    DataTable for listing packages for a project with
    - package name
    - package required version (as defined in composer.json)
    - package installed (as defined in composer.lock)
    - package update (newer version than the installed one, and still matching the requirements)
    """

    DEFAULT_CSS = """
        ComposerPackagesTable {
           border-title-color: $accent;
           border: $primary-background round;
           content-align: center middle;
        }
    """

    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.add_columns(*("Package", "Required", "Locked", "Upgrade", "Actions"))
        self.update_button = Text(" Update", style="bold")

    def set_requirements(
        self,
        required_packages: dict[str, str],
        locked_packages: dict[str, str],
        packages_updatable: dict[str, str],
    ) -> None:
        self.clear()
        for package, version in required_packages.items():
            styled_row = [
                Text(str(package), justify="left"),
                Text(str(version), style="italic #03AC13", justify="right"),
                Text(
                    str(locked_packages[package]) if package in locked_packages else "",
                    style="italic #FF0000",
                    justify="right",
                ),
                Text(
                    str(packages_updatable[package])
                    if package in packages_updatable
                    else "",
                    style="italic #00FF00",
                    justify="right",
                ),
                self.update_button if package in packages_updatable else "",
            ]
            self.add_row(*styled_row, key=package)

    @on(DataTable.CellSelected)
    def on_update_package_clicked(self, event: DataTable.CellSelected) -> None:
        if event.value == self.update_button:
            self.post_message(
                ComposerCommandRequested(
                    script=["update", event.cell_key.row_key.value],
                    allow_rerun=False,
                    refresh_composer_on_success=True,
                )
            )
