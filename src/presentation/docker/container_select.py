from textual.widgets import Select

from service_locator import ServiceContainer


class ContainerSelect(Select):
    def __init__(self, **kargs):
        super().__init__(
            (
                (docker_container.name, docker_container.id)
                for docker_container in ServiceContainer.docker_client().get_running_containers()
            ),
            **kargs
        )
