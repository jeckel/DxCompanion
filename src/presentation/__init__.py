from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TabbedContent, TabPane

from models import Project
from service_locator import ServiceContainer
from .component.message import TerminalCommandRequested

from .composer import ComposerCommandRequested
from .docker import DockerContainer
from .summary import ProjectSummaryContainer
from .component import Sidebar, TerminalModal, NonShellCommand


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

    def __init__(self):
        self._project = ServiceContainer.context().current_project
        super().__init__()
        self.title = f"DX Companion - {self._project.name}"

    def compose(self) -> ComposeResult:
        yield Sidebar(classes="-hidden")
        yield Header()
        with TabbedContent(initial="summary-pan"):
            with TabPane(title="Summary", id="summary-pan"):
                yield ProjectSummaryContainer(project=self._project)
            with TabPane(title="Docker", id="docker-pan"):
                yield DockerContainer(project=self._project)
        yield Footer()

    def action_toggle_sidebar(self) -> None:
        self.query_one(Sidebar).toggle_class("-hidden")

    @on(ComposerCommandRequested)
    def action_composer_script(self, event: ComposerCommandRequested) -> None:
        def refresh_composer(result: bool | None):
            if event.refresh_composer_on_success and result:
                ServiceContainer.composer_client().reset_updatable_packages()

        self.query_one(Sidebar).add_class("-hidden")
        self.app.push_screen(
            TerminalModal(
                command=NonShellCommand(
                    path=self._project.path,
                    command=event.command,
                ),
                allow_rerun=event.allow_rerun,
            ),
            refresh_composer,
        )

    @on(TerminalCommandRequested)
    def action_terminal_command(self, event: TerminalCommandRequested) -> None:
        self.query_one(Sidebar).add_class("-hidden")
        self.app.push_screen(
            TerminalModal(
                command=event.command,
                allow_rerun=event.allow_rerun,
            )
        )
