from textual import on
from textual.app import ComposeResult
from textual.events import ScreenResume
from textual.screen import Screen
from textual.widgets import Header, Footer

from presentation.component.sidebar import Sidebar
from .container import PackageManagerContainer
from service_locator import ServiceLocator


class PackageManagerScreen(Screen):
    BINDINGS = {
        ("escape", "return", "Return to project"),
    }

    def compose(self) -> ComposeResult:
        yield Sidebar(classes="-hidden")
        yield Header()
        project = ServiceLocator.context().current_project
        if len(project.package_managers) > 1:
            pass
            # @todo : add tabs per package manager
        else:
            yield PackageManagerContainer(project.package_managers[0])
        yield Footer()

    def action_return(self):
        self.app.switch_screen("summary")

    @on(ScreenResume)
    def screen_resume(self):
        pass
