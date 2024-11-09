from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button
from textual.worker import Worker, WorkerState

from models.composer import Composer
from service_locator import ServiceLocator

from .composer_packages_table import ComposerPackagesTable
from .composer_script_button import ComposerScriptButton


class ComposerContainer(Container):
    DEFAULT_CSS = """
        ComposerContainer {
            Container {
                layout: grid;
                grid-size: 1 3;

                #composer-packages-table {
                    row-span: 2;
                }
            }
            #composer-actions {
                height: 3;
            }
        }
    """

    def __init__(self, **kwargs):
        self._project = ServiceLocator.context().current_project
        self.composer = Composer.from_json(self._project.path)
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Container():
            yield ComposerPackagesTable(
                title="Composer packages", id="composer-packages-table"
            )
            yield ComposerPackagesTable(
                title="Composer packages-dev", id="composer-packages-dev-table"
            )
        with Horizontal(id="composer-actions"):
            yield ComposerScriptButton(
                script="install", label="Install", classes="ml-1"
            )
            yield ComposerScriptButton(
                script="update", label="Update all", refresh_composer_on_success=True
            )
            yield Button.success(
                "Refresh", id="composer-refresh-button", classes="ml-1"
            )

    def action_refresh(self) -> None:
        self.loading = True
        self._load_composer()

    async def on_mount(self):
        self.loading = True
        self._load_composer()

    @work(exclusive=True, thread=True)
    async def _load_composer(self) -> dict[str, str]:
        return ServiceLocator.composer_client().updatable_packages()

    @on(Worker.StateChanged)
    async def refresh_packages(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.state != WorkerState.SUCCESS:
            return
        packages_updatable = event.worker.result
        composer = ServiceLocator.composer_client().composer_json(self._project)
        package_table: ComposerPackagesTable = self.query_one(
            "#composer-packages-table"
        )
        package_table.set_requirements(
            composer.required_packages,
            composer.locked_packages,
            packages_updatable,
        )
        package_dev_table: ComposerPackagesTable = self.query_one(
            "#composer-packages-dev-table"
        )
        package_dev_table.set_requirements(
            composer.required_packages_dev,
            composer.locked_packages_dev,
            packages_updatable,
        )
        self.loading = False

    @on(Button.Pressed, "#composer-refresh-button")
    def on_refresh_pressed(self):
        ServiceLocator.composer_client().reset_updatable_packages()
        self.action_refresh()
