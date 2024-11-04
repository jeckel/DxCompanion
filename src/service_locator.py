from dependency_injector import containers, providers

from models.app_context import AppContext
from services import DockerClient, ComposerClient


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    docker_client = providers.Singleton(DockerClient)
    context = providers.Singleton(AppContext)
    composer_client = providers.Singleton(ComposerClient, context=context)
    # project = providers.Factory(Project)

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
