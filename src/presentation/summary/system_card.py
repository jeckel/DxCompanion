from rich.style import Style
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

from service_locator import ServiceLocator


class SystemCard(Container):
    DEFAULT_CSS = """
    SystemCard {
        height: auto;
        width: 45;
        border: $primary-background round;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._system_panel = Static(id="system_panel")

    def compose(self) -> ComposeResult:
        yield self._system_panel

    def on_mount(self) -> None:
        table = Table(
            show_header=False,
            box=None,
            title="System status",
            title_style=Style(color="#bbc8e8", bold=True),
        )
        table.add_column()
        table.add_column(min_width=25, max_width=27)
        system_status = ServiceLocator.system_status()
        self._add_system_row(table, "Php", system_status.php_version())
        self._add_system_row(table, "Composer", system_status.composer_version())
        self._add_system_row(table, "Symfony-Cli", system_status.symfony_version())
        self._add_system_row(table, "Castor", system_status.castor_version())
        self._add_system_row(table, "Docker", system_status.docker_version())
        self._add_system_row(table, "Ansible", system_status.ansible_version())

        self._system_panel.update(table)

    @staticmethod
    def _add_system_row(table: Table, label: str, version: str|None) -> None:
        table.add_row(
            f"[label]{label}:",
            f"[blue]{version}" if version is not None else "[orange1]N/A",
        )
