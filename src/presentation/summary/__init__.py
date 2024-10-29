from textual.containers import Container
from textual.widgets import Markdown

from models import Project


# service: Service = Provide[Container.service]
class ProjectSummaryContainer(Container):
    BORDER_TITLE = "Project's summary"
    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs)

    def compose(self):
        yield Markdown(
            f"""
# Project : {self.project.project_name}
"""
        )
