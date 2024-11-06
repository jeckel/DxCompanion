from typing import Optional

from rich.style import Style
from rich.table import Table
from textual import work, on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button
from textual.worker import Worker, WorkerState

from models.composer import Composer
from presentation.composer.composer_screen import ComposerScreen
from service_locator import ServiceLocator


class ComposerCard(Container):
    DEFAULT_CSS = """
    ComposerCard {
        width: 45;
    }
    """
    BORDER_TITLE = "Composer status"

    _composer: Optional[Composer] = None
    _packages_updatable: dict[str, str] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs, classes="card")
        self._project = ServiceLocator.context().current_project
        self._composer_panel = Static(id="composer_panel")

    def compose(self) -> ComposeResult:
        yield self._composer_panel
        yield Button("[underline]Manage packages", id="toggle_composer_tab")

    def on_mount(self) -> None:
        self._composer = ServiceLocator.composer_client().composer_json(
            self._project
        )
        self._composer_panel.update(self.get_composer_panel())
        self.query_one(Button).loading = True
        self._load_composer()

    def get_composer_panel(self) -> Table:
        table = Table(
            show_header=False,
            box=None,
            # title="Composer status",
            # title_style=Style(color="#bbc8e8", bold=True),
        )
        table.add_column()
        table.add_column(min_width=25, max_width=27)
        table.add_row(
            "[label]Composer:",
            "[green]Enabled" if self._project.composer else "[red]Disabled",
        )

        if self._project.composer and self._composer is not None:
            updatable_packages_keys = self._packages_updatable.keys()
            updatable_packages = len(
                set(self._composer.required_packages.keys()) & set(updatable_packages_keys)
            )
            if updatable_packages > 0:
                table.add_row(
                    "[label]Packages:",
                    f"[blue]{len(self._composer.required_packages)}[/blue] ([orange1]{updatable_packages} updates available[/orange1])",
                )
            else:
                table.add_row(
                    "[label]Packages:",
                    f"[blue]{len(self._composer.required_packages)}",
                )

            updatable_packages_dev = len(
                set(self._composer.required_packages_dev.keys()) & set(updatable_packages_keys)
            )
            if updatable_packages_dev > 0:
                table.add_row(
                    "[label]Packages-dev:",
                    f"[blue]{len(self._composer.required_packages_dev)}[/blue] "
                    f"([orange1]{updatable_packages_dev} updates available[/orange1])",
                )
            else:
                table.add_row(
                    "[label]Packages-dev:",
                    f"[blue]{len(self._composer.required_packages_dev)}",
                )
            return table

    @work(exclusive=True, thread=True)
    async def _load_composer(self, no_cache: bool = False) -> dict[str, str]:
        return ServiceLocator.composer_client().updatable_packages()

    @on(Worker.StateChanged)
    async def refresh_listview(self, event: Worker.StateChanged) -> None:
        if event.state != WorkerState.SUCCESS:
            return
        self._packages_updatable = event.worker.result
        self._composer_panel.update(self.get_composer_panel())
        self.query_one(Button).loading = False

    @on(Button.Pressed, "#toggle_composer_tab")
    def on_composer_manage(self):
        self.app.push_screen(ComposerScreen())
