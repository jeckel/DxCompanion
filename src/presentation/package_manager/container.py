from textual import work, on
from textual.containers import Container, Horizontal
from textual.app import ComposeResult
from textual.widgets import Button
from textual.worker import Worker, WorkerState

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

    def compose(self) -> ComposeResult:
        with Container():
            yield PackagesTable(
                title="Packages",
                packages=self._package_manager.project_packages(),
                id="packages_table",
            )
            yield PackagesTable(
                title="Packages-dev",
                packages=self._package_manager.project_packages("dev"),
                id="packages_dev_table",
            )
        with Horizontal(id="package_manager_actions"):
            yield Button(label="Install", classes="ml-1", id="install_packages")
            yield Button(label="Update all", id="update_packages")
            yield Button.success(label="Refresh", id="refresh_packages", classes="ml-1")

    def on_mount(self) -> None:
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

        table = self.query_one("#packages_table")
        assert isinstance(table, PackagesTable)
        table.refresh_table(event.worker.result["main"])

        table = self.query_one("#packages_dev_table")
        assert isinstance(table, PackagesTable)
        table.refresh_table(event.worker.result["dev"])

    @on(Button.Pressed, "#install_packages")
    def install_packages(self) -> None:
        self.app.push_screen(
            TerminalModal(
                command=self._package_manager.get_install_command(), allow_rerun=False
            ),
        )
