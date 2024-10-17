from textual import work, on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import TabPane
from textual.worker import Worker, WorkerState

from composer_utils import composer_updatable
from models.composer import Composer
from . import ComposerScriptButton, ComposerPackagesTable
from presentation.component import TerminalModal


class ComposerPan(TabPane):
    def __init__(self, composer_dir: str, **kwargs):
        self.composer_dir = composer_dir
        self.composer = Composer.from_json(composer_dir)
        super().__init__(**kwargs, title="Composer", id="composer-pan")


    def compose(self) -> ComposeResult:
        with Container():
            yield ComposerPackagesTable(title="Composer packages", id="composer-packages-table")
            yield ComposerPackagesTable(title="Composer packages-dev", id="composer-packages-dev-table")
        yield Horizontal(id="composer-actions")


    async def on_mount(self):
        self.loading = True
        self._load_composer()


    @work(exclusive=True, thread=True)
    async def _load_composer(self) -> dict[str, str]:
        # return {}
        return composer_updatable(self.composer_dir)


    @on(Worker.StateChanged)
    async def refresh_listview(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.state == WorkerState.SUCCESS:
            packages_updatable = event.worker.result
            table : ComposerPackagesTable = self.query_one("#composer-packages-table")
            table.set_requirements(self.composer.required_packages, self.composer.locked_packages, packages_updatable)
            table : ComposerPackagesTable = self.query_one("#composer-packages-dev-table")
            table.set_requirements(self.composer.required_packages_dev, self.composer.locked_packages_dev, packages_updatable)

            scripts = self.query_one("#composer-actions")
            for script in self.composer.manual_scripts:
                # self.log(f"Bouton {script}")
                new_button = ComposerScriptButton(script_name=script)
                await scripts.mount(new_button)

            self.loading = False


    @on(ComposerScriptButton.Pressed)
    def on_pressed(self, event: ComposerScriptButton.Pressed) -> None:
        if isinstance(event.button, ComposerScriptButton):
            self.app.push_screen(TerminalModal(command=['composer', '--no-ansi', event.button.script_name], path=self.composer_dir, use_stderr=True))