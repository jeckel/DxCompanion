import os
from enum import Enum

import docker
import yaml

from models.app_context import AppContext
from .base_service import BaseService


class ContainerStatus(Enum):
    NA = "n/a"
    RUNNING = "Running"

class DockerClient(BaseService):
    def __init__(self, context: AppContext):
        self._client = docker.from_env()
        self._context = context

    def get_running_containers(self) -> list:
        """
        Fetches a list of running containers.
        """
        return self._client.containers.list(all=True)

    def get_container_logs(self, container_id):
        """
        Fetches logs from a specific container.
        """
        container = self._client.containers.get(container_id)
        return container.logs(stream=True, follow=True)

    def list_container_names(self) -> dict[str, str]:
        """
        List docker containers names and their statuses.
        """
        project = self._context.current_project
        basename = os.path.basename(project.path)
        container_names = {}
        running_containers = self.get_running_containers()
        for compose_file in project.docker_compose_files:
            file_path = os.path.join(project.path, compose_file)
            with open(file_path, 'r') as file:
                docker_compose = yaml.safe_load(file)

            services = docker_compose.get("services", {})
            for service_name, service_config in services.items():
                container_name = service_config.get("container_name", f"{basename}-{service_name}")
                container_names[container_name] = ContainerStatus.NA.value

                for running_container in running_containers:
                    if running_container.name.startswith(container_name):
                        status = running_container.status
                        if "Health" in running_container.attrs["State"]:
                            status += f" ({running_container.attrs["State"]["Health"]["Status"]})"
                        container_names[container_name] = status
                        break

        return container_names
