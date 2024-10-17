from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import TabPane, Label

from models import Project


class ProjectSummaryPan(TabPane):
    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs, title="Summary", id="summary-pan")

    def compose(self) -> ComposeResult:
        with Container(id="project_summary"):
            yield Label(Text(str("Project :"), style="italic #03AC13", justify="right"))
            yield Label(Text(str(self.project.name), style="italic"))