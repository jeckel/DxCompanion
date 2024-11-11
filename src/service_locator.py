from dependency_injector import containers, providers

from models.app_context import AppContext
from services import DockerClient, SystemStatus
from services.package_manager import ComposerPackageManager


class ServiceLocator(containers.DeclarativeContainer):
    config = providers.Configuration()
    context = providers.Singleton(AppContext)
    docker_client = providers.Singleton(DockerClient, context=context)
    system_status = providers.Singleton(SystemStatus)
    composer_package_manager = providers.Singleton(
        ComposerPackageManager, context=context
    )
    package_manager = providers.Dict(
        composer=providers.Singleton(ComposerPackageManager, context=context)
    )
