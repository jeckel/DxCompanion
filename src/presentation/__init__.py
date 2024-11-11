from textual import on
from textual.app import App
from textual.css.query import NoMatches

from models import Project
from service_locator import ServiceLocator
from .component.message import TerminalCommandRequested

from .docker import DockerContainer
from .package_manager import PackageManagerScreen
from .summary import ProjectSummaryContainer
from .component import Sidebar, TerminalModal
from .summary.summary_screen import SummaryScreen


class MainApp(App[None]):
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
    SCREENS = {
        "summary": SummaryScreen,
        "packages": PackageManagerScreen,
    }

    _project: Project

    def __init__(self):
        super().__init__()
        self._project = ServiceLocator.context().current_project
        self.title = f"DX Companion - {self._project.name}"
        if self._project.has_package_managers:
            self.bind(
                keys="ctrl+u", action="toggle_package_screen", description="Packages"
            )

    def on_mount(self) -> None:
        self.push_screen("summary")

    def action_toggle_sidebar(self) -> None:
        try:
            self.query_one(Sidebar).toggle_class("-hidden")
        except NoMatches:
            pass

    def action_toggle_package_screen(self) -> None:
        self.switch_screen("packages")

    @on(TerminalCommandRequested)
    def action_terminal_command(self, event: TerminalCommandRequested) -> None:
        self.query_one(Sidebar).add_class("-hidden")
        self.app.push_screen(
            TerminalModal(
                command=event.command,
                allow_rerun=event.allow_rerun,
            )
        )
