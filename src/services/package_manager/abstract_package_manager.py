from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from models.app_context import AppContext
from services.base_service import BaseService


@dataclass
class Package:
    name: str
    required: Optional[str] = None
    locked: Optional[str] = None
    update: Optional[str] = None


class AbstractPackageManager(ABC, BaseService):
    """
    Abstract class for all package managers
    """

    _PACKAGE_MANAGER_LABEL: str | None = None

    def __init__(self, context: AppContext):
        self._context = context

    @property
    def label(self) -> str:
        return (
            self._PACKAGE_MANAGER_LABEL
            if self._PACKAGE_MANAGER_LABEL is not None
            else "Packages"
        )

    @abstractmethod
    def project_packages(self, group: Optional[str] = None) -> dict[str, Package]:
        """
        List all required and locked packages for the current project and given group
        :param group: The group to list packages for (example: dev)
        :return:
            list of packages with their required and locked version
        """

    @abstractmethod
    async def project_packages_with_updatable(
        self, group: Optional[str] = None
    ) -> dict[str, Package]:
        """
        Async list all required and locked packages for the current project and given group, will try to retrieve if an
        update of each package is available
        :param group: The group to list packages for (example: dev)
        :return:
            list of packages with their required, locked and update version
        """
