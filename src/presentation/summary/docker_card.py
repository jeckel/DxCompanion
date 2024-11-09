from rich.table import Table
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, Button

from service_locator import ServiceLocator


class DockerCard(Container):
    DEFAULT_CSS = """
    DockerCard {
        width: 60;
    }
    """
    BORDER_TITLE = "Docker containers"

    def __init__(self, **kwargs):
        super().__init__(**kwargs, classes="card")
        self._docker_panel = Static(id="system_panel")

    def compose(self) -> ComposeResult:
        yield self._docker_panel
        yield Button("[underline]Refresh", id="refresh-docker_panel")

    def on_mount(self) -> None:
        table = Table(
            show_header=False,
            box=None,
        )
        table.add_column()
        table.add_column()
        docker_client = ServiceLocator.docker_client()
        for container, status in docker_client.list_container_names().items():
            table.add_row(
                f"[label]{container}",
                f"[{self._color_by_status(status)}]{status.capitalize()}",
            )
        self._docker_panel.update(table)

    @staticmethod
    def _color_by_status(status: str) -> str:
        if status == "running" or status == "running (healthy)":
            return "green"
        elif status == "paused" or status.startswith("running ("):
            return "yellow"
        elif status.startswith("exited"):
            return "red"
        else:
            return "grey39"

    @on(Button.Pressed, "#refresh-docker_panel")
    def refresh_docker_panel(self) -> None:
        self.on_mount()
