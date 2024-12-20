from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer, TabbedContent, TabPane

from presentation import Sidebar, DockerContainer
from .summary_container import ProjectSummaryContainer
from service_locator import ServiceLocator


class SummaryScreen(Screen):
    """
    Screen to display project summary
    """

    BINDINGS = {
        ("c", "toggle_composer_screen", "Composer"),
    }

    def compose(self) -> ComposeResult:
        yield Sidebar(classes="-hidden")
        yield Header()
        with TabbedContent(initial="summary-pan"):
            with TabPane(title="Summary", id="summary-pan"):
                yield ProjectSummaryContainer()
            if ServiceLocator.docker_client().has_containers():
                with TabPane(title="Docker", id="docker-pan"):
                    yield DockerContainer(
                        project=ServiceLocator.context().current_project
                    )
        yield Footer()

    @on(ScreenResume)
    def screen_resume(self):
        self.query_one(ProjectSummaryContainer).refresh_packages()

    def action_toggle_composer_screen(self):
        self.app.switch_screen("composer")
