from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Header, Footer, Button, DataTable, Label

from models import Project
from .composer import ComposerRequireTable, ComposerScripts


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
        with Container(id="project_container"):
            with Container(id="project_summary"):
                yield Label(Text(str("Project :"), style="italic #03AC13", justify="right"))
                yield Label(Text(str(self._project.name), style="italic"))
                yield ComposerScripts(id="composer_scripts")
            yield ComposerRequireTable(title="Composer requirements", id="composer_table")

        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(ComposerRequireTable)
        table.set_requirements(self._project.composer_json.require)


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    @on(Button.Pressed, "#get_pocket_button")
    def on_get_pocket_button_pressed(self, event: Button.Pressed) -> None:
        pass
        # self.push_screen('get_pocket')


