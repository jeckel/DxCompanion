from dependency_injector import containers, providers

from models.app_context import AppContext
from services import DockerClient, ComposerClient, SystemStatus


class ServiceLocator(containers.DeclarativeContainer):
    config = providers.Configuration()
    docker_client = providers.Singleton(DockerClient)
    context = providers.Singleton(AppContext)
    composer_client = providers.Singleton(ComposerClient, context=context)
    system_status = providers.Singleton(SystemStatus)
