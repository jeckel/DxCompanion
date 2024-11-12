from typing import Optional

from textual import work, on
from textual.containers import Container, Horizontal
from textual.app import ComposeResult
from textual.widgets import Button, DataTable
from textual.worker import Worker, WorkerState
from textual.css.query import NoMatches

from .packages_table import PackagesTable
from service_locator import ServiceLocator
from services.package_manager.abstract_package_manager import Package
from presentation.component import TerminalModal


class PackageManagerContainer(Container):
    DEFAULT_CSS = """
        PackageManagerContainer {
            Container {
                layout: grid;
                grid-size: 1 3;

                #packages_table {
                    row-span: 2;
                }
            }
            #package_manager_actions {
                height: 3;
            }
        }
    """

    _packages: dict[str, Package] = {}
    _packages_dev: dict[str, Package] = {}

    def __init__(self, package_manager: str, **kwargs):
        self._package_manager = ServiceLocator.package_manager()[package_manager]
        super().__init__(**kwargs)
        self._package_table = PackagesTable(
            title="Packages",
            packages=self._package_manager.project_packages(),
            allow_update=self._package_manager.has_update_package_command(),
            id="packages_table",
        )
        self._package_dev_table = PackagesTable(
            title="Packages-dev",
            packages=self._package_manager.project_packages("dev"),
            allow_update=self._package_manager.has_update_package_command(),
            id="packages_dev_table",
        )

    def compose(self) -> ComposeResult:
        """
        Compose the package manager container with both packages tables and an action button bar at the bottom
        """
        with Container():
            yield self._package_table
            yield self._package_dev_table
        with Horizontal(id="package_manager_actions"):
            if self._package_manager.has_install_command():
                yield Button(label="Install", classes="ml-1", id="install_packages")
            if self._package_manager.has_update_all_command():
                yield Button(label="Update all", id="update_packages")
            yield Button.success(label="Refresh", id="refresh_packages", classes="ml-1")

    def _disable(self):
        """
        Disable the container by setting the table with loading state and disabling the action buttons
        """
        self._package_table.loading = True
        self._package_dev_table.loading = True
        if self._package_manager.has_install_command():
            self.query_one("#install_packages").disabled = True
        if self._package_manager.has_update_all_command():
            self.query_one("#update_packages").disabled = True
        self.query_one("#refresh_packages").disabled = True

    def _enable(self):
        """
        Enable the container by setting the table with loading state to false and enabling the action buttons
        """
        self._package_table.loading = False
        self._package_dev_table.loading = False
        if self._package_manager.has_install_command():
            self.query_one("#install_packages").disabled = False
        if self._package_manager.has_update_all_command():
            self.query_one("#update_packages").disabled = False
        self.query_one("#refresh_packages").disabled = False

    def on_mount(self) -> None:
        self._disable()
        self._load_updates()

    def reload_table(self, table: Optional[DataTable] = None) -> None:
        if table is None:
            self._disable()
        else:
            table.loading = True
        self._package_manager.reset_updatable_packages()
        self._load_updates()

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

        self._package_table.refresh_table(event.worker.result["main"])
        self._package_dev_table.refresh_table(event.worker.result["dev"])
        self._enable()

    @on(Button.Pressed, "#refresh_packages")
    def refresh_packages(self):
        self.reload_table()

    @on(Button.Pressed, "#install_packages")
    def install_packages(self) -> None:
        self.app.push_screen(
            TerminalModal(
                command=self._package_manager.get_install_command(), allow_rerun=False
            ),
        )

    @on(Button.Pressed, "#update_packages")
    def update_packages(self) -> None:
        self.app.push_screen(
            TerminalModal(
                command=self._package_manager.get_update_all_command(),
                allow_rerun=False,
            ),
            callback=lambda result: self.reload_table() if result else None,
        )

    @on(DataTable.CellSelected)
    def on_update_package_clicked(self, event: DataTable.CellSelected) -> None:
        if event.cell_key.column_key.value == "update":
            self.app.push_screen(
                TerminalModal(
                    command=self._package_manager.get_update_package_command(
                        event.cell_key.row_key.value
                    ),
                    allow_rerun=False,
                ),
                callback=lambda result: self.reload_table(event.data_table)
                if result
                else None,
            )
