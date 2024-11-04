from textual.containers import Container
from textual.widgets import Markdown

from models import Project
from .composer_card import ComposerCard


# service: Service = Provide[Container.service]
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

    def __init__(self, project: Project, **kwargs):
        self._project = project
        super().__init__(**kwargs)

    def compose(self):
        yield Markdown(
            f"""
# Project : {self._project.project_name}
"""
        )
        yield ComposerCard(project=self._project)
