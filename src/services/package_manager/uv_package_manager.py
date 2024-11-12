from typing import Optional

from models import CommandType
from .abstract_package_manager import AbstractPackageManager, Package


class UvPackageManager(AbstractPackageManager):
    def project_packages(self, group: Optional[str] = None) -> dict[str, Package]:
        return {}

    async def project_packages_with_updatable(
        self, group: Optional[str] = None
    ) -> dict[str, Package]:
        return {}

    def reset_updatable_packages(self) -> None:
        pass

    @staticmethod
    def has_install_command() -> bool:
        return False

    def get_install_command(self) -> CommandType:
        raise NotImplementedError

    @staticmethod
    def has_update_all_command() -> bool:
        return False

    def get_update_all_command(self) -> CommandType:
        raise NotImplementedError

    @staticmethod
    def has_update_package_command() -> bool:
        return False

    def get_update_package_command(self, package_name: str) -> CommandType:
        raise NotImplementedError

    def custom_commands(self) -> dict[str, CommandType]:
        return {}
