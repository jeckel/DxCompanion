from textual.containers import Container
from textual.widgets import Markdown

from .composer_card import ComposerCard
from service_locator import ServiceContainer


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
        self._project = ServiceContainer.context().current_project

    def compose(self):
        yield Markdown(
            f"""
# Project : {self._project.project_name}
"""
        )
        yield ComposerCard()

    def refresh_composer(self):
        self.query_one(ComposerCard).on_mount()
