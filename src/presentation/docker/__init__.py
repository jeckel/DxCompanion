from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, TabPane

from models import Project


class DockerPan(TabPane):
    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs, title="Docker", id="docker-pan")

    def compose(self) -> ComposeResult:
        with Container(id="project_docker"):
            yield Label(
                Text(str("Work in progress"), style="italic #03AC13", justify="right")
            )
