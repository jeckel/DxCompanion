from textual import work, on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button
from textual.worker import Worker, WorkerState
from rich.style import Style
from rich.table import Table

from presentation import ComposerScreen
from service_locator import ServiceLocator
from services.package_manager.abstract_package_manager import Package


class PackageCard(Container):
    DEFAULT_CSS = """
    PackageCard {
        width: 45;
    }
    """
    BORDER_TITLE = "Packages status"

    def __init__(self, **kwargs):
        super().__init__(**kwargs, classes="card")

    def compose(self) -> ComposeResult:
        for (
            package_manager
        ) in ServiceLocator.context().current_project.package_managers:
            yield PackagePanel(package_manager=package_manager)
        yield Button("[underline]Manage packages", id="toggle_package_screen")

    @on(Button.Pressed, "#toggle_package_screen")
    def on_composer_manage(self):
        self.app.push_screen(ComposerScreen())

    def refresh_packages(self) -> None:
        """
        @todo search for all package panel and refresh them
        """


class PackagePanel(Static):
    _packages: dict[str, Package] = {}
    _packages_dev: dict[str, Package] = {}

    def __init__(self, package_manager: str, **kwargs):
        self._package_manager = ServiceLocator.package_manager()[package_manager]
        super().__init__(**kwargs)

    def on_mount(self) -> None:
        self._packages = self._package_manager.project_packages()
        self._packages_dev = self._package_manager.project_packages("dev")
        self.update(self._get_package_table())
        self._load_updates()

    def _get_package_table(self) -> Table:
        table = Table(
            show_header=False,
            box=None,
            title=f"{self._package_manager.label} status",
            title_style=Style(color="#bbc8e8", bold=True),
        )
        table.add_column()
        table.add_column(min_width=25, max_width=27)
        self._add_package_row(table, self._packages, "Packages")
        self._add_package_row(table, self._packages_dev, "Packages Dev")
        return table

    @staticmethod
    def _add_package_row(
        table: Table, packages: dict[str, Package], group_label: str
    ) -> None:
        updates = sum(1 for package in packages.values() if package.update is not None)
        if updates > 0:
            table.add_row(
                f"[label]{group_label}:",
                f"[blue]{len(packages)}[/blue] "
                f"([orange1]{updates} updates available[/orange1])",
            )
        else:
            table.add_row(
                f"[label]{group_label}:",
                f"[blue]{len(packages)}",
            )

    @work(exclusive=True, thread=True)
    async def _load_updates(self) -> dict[str, dict[str, Package]]:
        main_packages = await self._package_manager.project_packages_with_updatable()
        dev_packages = await self._package_manager.project_packages_with_updatable(
            group="dev"
        )
        return {"main": main_packages, "dev": dev_packages}

    @on(Worker.StateChanged)
    async def refresh_listview(self, event: Worker.StateChanged) -> None:
        if event.state != WorkerState.SUCCESS:
            return
        self._packages = event.worker.result["main"]
        self._packages_dev = event.worker.result["dev"]
        self.update(self._get_package_table())
