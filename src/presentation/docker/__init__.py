from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import TabPane, Button, Select, Static, Label

from models import Project
from textual import on

from presentation.docker.container_log_widget import ContainerLogWidget
from presentation.docker.container_select import ContainerSelect


class DockerContainer(Container):
    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs)
        self.docker_logs = ContainerLogWidget()

    def compose(self) -> ComposeResult:
        with Container():
            with Horizontal(id="docker_container_select_container"):
                yield Label("Container:")
                yield ContainerSelect()
                yield Button.success(" Refresh", id="docker_refresh")
            yield self.docker_logs

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.docker_logs.stream_logs(event.value)

    @on(Button.Pressed, "#docker_refresh")
    def refresh_container_list(self):
        self.query_one(ContainerSelect).refresh_container_list()
