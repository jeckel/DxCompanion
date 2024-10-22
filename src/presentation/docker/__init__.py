from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, TabPane, Button, RichLog

from models import Project
import subprocess
from textual.widgets import DataTable
from textual import work, on

from presentation.docker.container_table import ContainerTable


class DockerPan(TabPane):
    def __init__(self, project: Project, **kwargs):
        self.project = project
        super().__init__(**kwargs, title="Docker", id="docker-pan")
        self.data_table = ContainerTable(title="Containers", project=self.project, classes="table_container")
        self.docker_logs = RichLog(
                id="docker_log",
                highlight=True,
                markup=True,
                classes="modal_container",
            )

    def compose(self) -> ComposeResult:
        with Container(id="project_docker"):
            yield Button.success(" Refresh", id="docker_refresh")
            yield self.data_table
            yield self.docker_logs

    @on(Button.Pressed, "#docker_refresh")
    def action_refresh(self):
        self.data_table.refresh_containers()

    @on(DataTable.RowSelected)
    def on_docker_container_selected(self, event: DataTable.RowSelected) -> None:
        container_name = event.row_key.value
        self.docker_logs.write(f"Logs for container {container_name}:\n")

