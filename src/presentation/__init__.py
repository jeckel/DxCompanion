from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane
from textual.containers import Container

from models import Project

from .composer import ComposerContainer
from .docker import DockerContainer
from .summary import ProjectSummaryContainer
from .component import Sidebar



class MainApp(App[None]):
    """A Textual app to manage stopwatches."""

    TITLE = "DX Companion"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("ctrl+s", "toggle_sidebar", "Toggle sidebar"),
    ]
    DEFAULT_CSS = """
    Screen {
        layers: sidebar;
    }
    """
    CSS_PATH = "../tcss/layout.tcss"
    _project: Project

    def __init__(self, project: Project):
        self._project = project
        super().__init__()
        self.title = f"DX Companion - {project.name}"

    def compose(self) -> ComposeResult:
        yield Sidebar(project=self._project, classes="-hidden")
        yield Header()
        with TabbedContent(initial="summary-pan"):
            with TabPane(title="Summary", id="summary-pan"):
                yield ProjectSummaryContainer(project=self._project)
            with TabPane(title="Composer", id="composer-pan"):
                yield ComposerContainer(project=self._project)
            with TabPane(title="Docker", id="docker-pan"):
                yield DockerContainer(project=self._project)
        yield Footer()

    def action_toggle_sidebar(self) -> None:
        self.query_one(Sidebar).toggle_class("-hidden")