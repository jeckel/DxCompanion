from textual.widgets import DataTable
from textual import work, on
import subprocess
import docker

from models import Project


class ContainerTable(DataTable):
    """
    DataTable for listing docker containers for a project.
    """
    def __init__(self, title: str, project: Project, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.project = project
        self.add_columns(*("Name", "Image", "Command", "State"))
        self.cursor_type = "row"

    async def on_mount(self):
        self.refresh_containers()

    @work(exclusive=True, thread=True)
    async def refresh_containers(self):
        self.clear()

        client = docker.from_env()
        containers = client.containers.list()
        for container in containers:
            image = container.image.tags[0] if container.image.tags else "N/A"
            command = container.attrs['Config']['Cmd']
            created = container.attrs['State']['StartedAt']
            status = container.status
            self.add_row(*[container.name, image, " ".join(command), created, status], key=container.id)
