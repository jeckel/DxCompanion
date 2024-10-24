import docker

from .base_service import BaseService


class DockerClient(BaseService):
    def __init__(self):
        self.client = docker.from_env()

    def get_running_containers(self) -> list:
        """Fetches a list of running containers."""
        return self.client.containers.list()

    def get_container_logs(self, container_id):
        """Fetches logs from a specific container."""
        container = self.client.containers.get(container_id)
        return container.logs(stream=True, follow=True)
