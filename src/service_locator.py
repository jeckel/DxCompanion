from dependency_injector import containers, providers

from models import Project
from services import DockerClient, ComposerClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    docker_client = providers.Singleton(DockerClient)
    composer_client = providers.Singleton(ComposerClient)
    project = providers.Factory(Project)

    # api_client = providers.Singleton(
    #     ApiClient,
    #     api_key=config.api_key,
    #     timeout=config.timeout,
    # )
    #
    # service = providers.Factory(
    #     Service,
    #     api_client=api_client,
    # )
