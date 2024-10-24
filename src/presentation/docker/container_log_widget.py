from textual.widgets import RichLog
from textual import work

from service_locator import Container


class ContainerLogWidget(RichLog):
    def __init__(self, **kargs):
        super().__init__(id="docker_log", highlight=True, markup=True, **kargs)

    @work(exclusive=True, thread=True)
    def stream_logs(self, container_id: str):
        self.clear()
        self.border_title = f"Logs for container {container_id}"

        for log in Container.docker_client().get_container_logs(container_id):
            # Convert bytes to string and update the logs widget
            self.write(log.decode("utf-8").strip())
