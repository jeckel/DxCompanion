from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent

from models import Project

from .composer import ComposerPan
from .docker import DockerPan
from .summary import ProjectSummaryPan


class MainApp(App):
    """A Textual app to manage stopwatches."""

    TITLE = "DX Companion"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    CSS_PATH = "../tcss/layout.tcss"
    _project: Project

    def __init__(self, project: Project):
        self._project = project
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="summary-pan"):
            yield ProjectSummaryPan(project=self._project)
            yield ComposerPan(project=self._project)
            yield DockerPan(project=self._project)
        yield Footer()
