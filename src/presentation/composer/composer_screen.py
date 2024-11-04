from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer

from models import Project
from .composer_container import ComposerContainer
from presentation.component.sidebar import Sidebar


class ComposerScreen(Screen):
    BINDINGS = {
        ("escape", "return", "Return to project"),
    }

    def __init__(self, project: Project, **kwargs):
        self._project = project
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Sidebar(project=self._project, classes="-hidden")
        yield Header()
        yield ComposerContainer(self._project)
        yield Footer()

    def action_return(self):
        self.dismiss()
