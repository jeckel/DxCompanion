from typing import Optional

from rich.text import Text
from textual.widgets import DataTable
from textual import on

from services.package_manager.abstract_package_manager import Package


class PackagesTable(DataTable):
    """
    DataTable for listing packages for a project with
    - package name
    - package required version
    - package installed (as defined in lock file)
    - package update (newer version than the installed one, and still matching the requirements)
    """

    DEFAULT_CSS = """
        PackagesTable {
           border-title-color: $accent;
           border: $primary-background round;
           content-align: center middle;
        }
    """

    _packages: dict[str, Package] = {}

    def __init__(
        self,
        title: str,
        packages: dict[str, Package],
        allow_update: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.border_title = title
        self._packages = packages
        self._allow_update = allow_update
        self.add_columns(*("Package", "Required", "Locked", "Upgrade"))
        if self._allow_update:
            self.add_column(label="Actions", key="update")
        self.update_button = Text(" Update", style="bold")

    def on_mount(self):
        self.refresh_table()

    def refresh_table(self, packages: Optional[dict[str, Package]] = None) -> None:
        if packages is not None:
            self._packages = packages
        self.clear()
        for package in self._packages.values():
            styled_row = [
                Text(str(package.name), justify="left"),
                Text(str(package.required), style="italic #03AC13", justify="right"),
                Text(
                    str(package.locked),
                    style="italic #FF0000",
                    justify="right",
                ),
                Text(
                    str(package.update if package.update is not None else ""),
                    style="italic #00FF00",
                    justify="right",
                ),
            ]
            if self._allow_update:
                styled_row.append(
                    self.update_button if package.update is not None else ""
                )
            self.add_row(*styled_row, key=package.name)
