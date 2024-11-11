from textual.containers import Container
from textual.widgets import Markdown
from textual.css.query import NoMatches

from service_locator import ServiceLocator
from .docker_card import DockerCard
from .package_card import PackageCard
from .system_card import SystemCard


class ProjectSummaryContainer(Container):
    BORDER_TITLE = "Project's summary"
    DEFAULT_CSS = """
        ProjectSummaryContainer {
            border-title-color: $accent;
            border: $primary-background round;
            content-align: center middle;
            Markdown {
                height: auto;
            }
        }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._project = ServiceLocator.context().current_project

    def compose(self):
        yield Markdown(
            f"""
# Project : {self._project.project_name}
"""
        )
        if len(ServiceLocator.context().current_project.package_managers) > 0:
            yield PackageCard()
        yield SystemCard()
        yield DockerCard()

    def refresh_packages(self):
        try:
            self.query_one(PackageCard).refresh_packages()
        except NoMatches:
            pass
