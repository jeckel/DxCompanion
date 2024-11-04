from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer

from .composer_container import ComposerContainer
from presentation.component.sidebar import Sidebar


class ComposerScreen(Screen):
    BINDINGS = {
        ("escape", "return", "Return to project"),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Sidebar(classes="-hidden")
        yield Header()
        yield ComposerContainer()
        yield Footer()

    def action_return(self):
        self.dismiss()

    @on(ScreenResume)
    def screen_resume(self):
        self.query_one(ComposerContainer).action_refresh()
