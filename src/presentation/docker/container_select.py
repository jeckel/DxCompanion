from textual.widgets import Select

from service_locator import Container


class ContainerSelect(Select):
    def __init__(self, **kargs):
        super().__init__(
            ((docker_container.name, docker_container.id) for docker_container in Container.docker_client().get_running_containers()),
            **kargs
        )