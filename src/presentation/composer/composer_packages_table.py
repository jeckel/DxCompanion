from rich.text import Text
from textual.widgets import DataTable


class ComposerPackagesTable(DataTable):
    """
    DataTable for listing packages for a project with
    - package name
    - package required version (as defined in composer.json)
    - package installed (as defined in composer.lock)
    - package update (newer version than the installed one, and still matching the requirements)
    """

    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.cursor_type = "row"
        self.add_columns(*("Package", "Required", "Locked", "Upgrade"))

    def set_requirements(
        self,
        required_packages: dict[str, str],
        locked_packages: dict[str, str],
        packages_updatable: dict[str, str],
    ) -> None:
        for package, version in required_packages.items():
            styled_row = [
                Text(str(package), justify="left"),
                Text(str(version), style="italic #03AC13", justify="right"),
            ]
            if package in locked_packages:
                styled_row.append(
                    Text(
                        str(locked_packages[package]),
                        style="italic #FF0000",
                        justify="right",
                    )
                )
            else:
                styled_row.append("")
            if package in packages_updatable:
                styled_row.append(
                    Text(
                        str(packages_updatable[package]),
                        style="italic #00FF00",
                        justify="right",
                    )
                )
            else:
                styled_row.append("")
            self.add_row(*styled_row)
