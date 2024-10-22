from threading import Thread

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, TabPane, Button, RichLog
import docker

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
        self.stream_logs(container_name)

    @work(exclusive=True, thread=True)
    def stream_logs(self, container_id: str):
        # Create a Docker client
        self.docker_logs.clear()
        self.docker_logs.write(f"Logs for container {container_id}:\n")
        client = docker.from_env()
        container = client.containers.get(container_id)

        # Stream the logs from the container
        for log in container.logs(stream=True, follow=True):
            # Convert bytes to string and update the logs widget
            log_message = log.decode('utf-8').strip()
            self.docker_logs.write(log_message)
