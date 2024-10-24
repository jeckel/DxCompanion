from dependency_injector import containers, providers

from services import DockerClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    docker_client = providers.Singleton(DockerClient)

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
