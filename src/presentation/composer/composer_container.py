from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, TabPane
from textual.worker import Worker, WorkerState

from models import Project
from models.composer import Composer
from presentation.component import TerminalModal
from service_locator import Container as ServiceContainer

from .composer_packages_table import ComposerPackagesTable
from .composer_script_button import ComposerScriptButton


class ComposerContainer(Container):
    def __init__(self, project: Project, **kwargs):
        self.project = project
        self.composer = Composer.from_json(project.path)
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Container():
            yield ComposerPackagesTable(
                title="Composer packages", id="composer-packages-table"
            )
            yield ComposerPackagesTable(
                title="Composer packages-dev", id="composer-packages-dev-table"
            )
        yield Horizontal(id="composer-actions")

    async def on_mount(self):
        self.loading = True
        self._load_composer()

    @work(exclusive=True, thread=True)
    async def _load_composer(self) -> dict[str, str]:
        return ServiceContainer.composer_client().updatable_packages(self.project)

    @on(Worker.StateChanged)
    async def refresh_listview(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.state == WorkerState.SUCCESS:
            packages_updatable = event.worker.result
            composer = ServiceContainer.composer_client().composer_json(self.project)
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

            scripts = self.query_one("#composer-actions")
            await scripts.remove_children()

            await scripts.mount(ComposerScriptButton(script_name="install"))
            await scripts.mount(
                ComposerScriptButton(script_name="update", label="update all")
            )

            for script in self.composer.manual_scripts:
                # self.log(f"Bouton {script}")
                new_button = ComposerScriptButton(script_name=script)
                await scripts.mount(new_button)

            self.loading = False

    @on(ComposerScriptButton.Pressed)
    def on_pressed(self, event: Button.Pressed) -> None:
        if isinstance(event.button, ComposerScriptButton):
            self.app.push_screen(
                TerminalModal(
                    command=["composer", "--no-ansi", event.button.script_name],
                    path=self.project.path,
                    use_stderr=True,
                    allow_rerun=True,
                )
            )

    @on(ComposerPackagesTable.UpdatePackageClicked)
    def on_update_package_clicked(
        self, event: ComposerPackagesTable.UpdatePackageClicked
    ) -> None:
        self.app.push_screen(
            TerminalModal(
                command=["composer", "--no-ansi", "update", event.package],
                path=self.project.path,
                use_stderr=True,
            ),
            self.terminal_modal_callback,
        )

    def terminal_modal_callback(self, result: bool) -> None:
        if result:
            self.loading = True
            self._load_composer()
