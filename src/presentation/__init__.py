from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Header, Footer, Button, DataTable, Label

from composer_utils import composer_updatable
from models import Project
from .composer import ComposerRequireTable, ComposerScripts, ComposerScriptButton
from .terminal import TerminalModal


class MainApp(App):
    """A Textual app to manage stopwatches."""

    TITLE = "Project Manager"
    # SCREENS = {"get_pocket": GetPocketScreen}
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    CSS_PATH = "../tcss/layout.tcss"
    _project: Project

    def __init__(self, project: Project):
        self._project = project
        super().__init__()

    # BINDINGS = [("b", "", "GetPocketScreen")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ComposerScripts(id="composer_scripts")
        with Container(id="project_container"):
            with Container(id="project_summary"):
                yield Label(Text(str("Project :"), style="italic #03AC13", justify="right"))
                yield Label(Text(str(self._project.name), style="italic"))
                # yield ComposerScripts(id="composer_scripts")
            yield ComposerRequireTable(title="Composer requirements", id="composer_table")

        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one(ComposerRequireTable)
        packages_updatable = composer_updatable(self._project)
        table.set_requirements(
            self._project.composer_json.required_packages,
            self._project.composer_json.locked_packages,
            packages_updatable)
        scripts = self.query_one(ComposerScripts)
        for script in self._project.composer_json.manual_scripts:
            self.log(f"Bouton {script}")
            new_button = ComposerScriptButton(script_name=script)
            await scripts.mount(new_button)


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    @on(Button.Pressed)
    def on_pressed(self, event: Button.Pressed) -> None:
        if isinstance(event.button, ComposerScriptButton):
            # command = f"cd {self._project.path} && composer {event.button.script_name}"
            # self.log(command)
            self.push_screen(TerminalModal(command=['composer', event.button.script_name], path=self._project.path))
            # self.push_screen(TerminalModal(command='ls -lah', path=self._project.path))
        # else:
        #     self.pop_screen()


