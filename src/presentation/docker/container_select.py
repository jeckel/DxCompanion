from textual.widgets import Select

from service_locator import ServiceLocator


class ContainerSelect(Select):
    def __init__(self, **kargs):
        super().__init__(
            (
                (docker_container.name, docker_container.id)
                for docker_container in ServiceLocator.docker_client().get_running_containers()
            ),
            **kargs
        )

    def refresh_container_list(self):
        self.clear()
        self.set_options(
            (docker_container.name, docker_container.id)
            for docker_container in ServiceLocator.docker_client().get_running_containers()
        )
