import subprocess
from typing import Optional

from models import Project, CommandType, NonShellCommand
from models.composer import Composer
from services.package_manager.abstract_package_manager import (
    AbstractPackageManager,
    Package,
)


class ComposerPackageManager(AbstractPackageManager):
    """
    Concrete implementation of AbstractPackageManager for Composer
    """

    _PACKAGE_MANAGER_LABEL = "Composer"

    def project_packages(self, group: Optional[str] = None) -> dict[str, Package]:
        if self._context.project is None:
            return {}
        composer = self.composer_json(self._context.project)
        if composer is None:
            return {}
        if group is None:
            packages = composer.required_packages
            packages_locked = composer.locked_packages
        elif group == "dev":
            packages = composer.required_packages_dev
            packages_locked = composer.locked_packages_dev
        else:
            raise ValueError(
                f"Unsupported group: {group}, only supports 'dev' or None group"
            )
        to_return = {}
        for package_name, version in packages.items():
            to_return[package_name] = Package(
                name=package_name,
                required=version,
                locked=packages_locked.get(package_name),
            )
        return to_return

    async def project_packages_with_updatable(
        self, group: Optional[str] = None
    ) -> dict[str, Package]:
        packages = self.project_packages(group)
        updatable_packages = self.updatable_packages()
        for package_name, package in packages.items():
            if package_name in updatable_packages:
                package.update = updatable_packages[package_name]
        return packages

    @staticmethod
    def composer_json(project: Project) -> None | Composer:
        if not project.composer:
            return None
        return Composer.from_json(project.path)

    def updatable_packages(self) -> dict[str, str]:
        project = self._context.current_project

        if self._context.composer_updatable_packages is not None:
            return self._context.composer_updatable_packages

        with subprocess.Popen(
            ["composer", "update", "--dry-run", "--no-ansi", "-n"],
            cwd=project.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            stdout, stderr = process.communicate()
            lines = stderr.strip().split("\n")
            packages: dict[str, str] = {}

            # Processing lines for packages
            for line in lines:
                if line.startswith("  - Upgrading"):
                    parts = line.split("(")
                    package_name = line.strip().split(" ")[2]
                    version_info = parts[1].strip().rstrip(")")
                    target_version = version_info.split("=>")[-1].strip()
                    packages[package_name] = target_version
            self._context.composer_updatable_packages = packages
        return self._context.composer_updatable_packages

    def reset_updatable_packages(self) -> None:
        self._context.composer_updatable_packages = None

    def get_install_command(self) -> CommandType:
        return NonShellCommand(
            path=self._context.current_project.path,
            command=["composer", "install", "--no-ansi", "-n"],
        )

    def get_update_all_command(self) -> CommandType:
        return NonShellCommand(
            path=self._context.current_project.path,
            command=["composer", "update", "--no-ansi", "-n"],
        )

    def get_update_package_command(self, package_name: str) -> CommandType:
        return NonShellCommand(
            path=self._context.current_project.path,
            command=["composer", "update", package_name, "--no-ansi", "-n"],
        )

    def custom_commands(self) -> dict[str, CommandType]:
        commands: dict[str, CommandType] = {}
        if self._context.project is None:
            return commands
        composer = self.composer_json(self._context.project)
        if composer is None:
            return commands
        for script in composer.manual_scripts:
            commands[script] = NonShellCommand(
                path=self._context.current_project.path,
                label=script.capitalize(),
                command=["composer", script, "--no-ansi", "-n"],
            )
        return commands
