from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Header, Footer, Button

from models import Project

class MainApp(App):
    """A Textual app to manage stopwatches."""

    TITLE = "Project Manager"
    # SCREENS = {"get_pocket": GetPocketScreen}
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    _project: Project

    def __init__(self, project: Project):
        self._project = project
        super().__init__()
        # self.dark = False

    # BINDINGS = [("b", "", "GetPocketScreen")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container():
            yield Button(f"Composer {self._project.name}", id='get_pocket_button')
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    @on(Button.Pressed, "#get_pocket_button")
    def on_get_pocket_button_pressed(self, event: Button.Pressed) -> None:
        pass
        # self.push_screen('get_pocket')


