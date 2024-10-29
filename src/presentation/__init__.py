from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from models import Project

from .composer import ComposerContainer
from .docker import DockerContainer
from .summary import ProjectSummaryContainer


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
        self.title = f"DX Companion - {project.name}"

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="summary-pan"):
            with TabPane(title="Summary", id="summary-pan"):
                yield ProjectSummaryContainer(project=self._project)
            with TabPane(title="Composer", id="composer-pan"):
                yield ComposerContainer(project=self._project)
            with TabPane(title="Docker", id="docker-pan"):
                yield DockerContainer(project=self._project)
        yield Footer()
