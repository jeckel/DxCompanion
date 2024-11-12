import os
import subprocess
import tomllib
import re
import json
from typing import Optional

from models import CommandType, NonShellCommand
from .abstract_package_manager import AbstractPackageManager, Package


class UvPackageManager(AbstractPackageManager):
    def project_packages(self, group: Optional[str] = None) -> dict[str, Package]:
        locked_versions = self._get_locked_versions()
        return {
            package: Package(package, version, locked_versions[package])
            for package, version in self._get_required_packages(group).items()
        }

    async def project_packages_with_updatable(
        self, group: Optional[str] = None
    ) -> dict[str, Package]:
        packages = self.project_packages(group)
        updates = self._get_updatable_versions()
        for package, version in updates.items():
            if package in packages:
                packages[package].update = version
        return packages

    def reset_updatable_packages(self) -> None:
        pass

    def get_install_command(self) -> CommandType:
        return NonShellCommand(
            path=self._context.current_project.path,
            command=["uv", "sync"],
        )

    def get_update_all_command(self) -> CommandType:
        return NonShellCommand(
            path=self._context.current_project.path,
            command=["uv", "sync", "--upgrade"],
        )

    def get_update_package_command(self, package_name: str) -> CommandType:
        return NonShellCommand(
            path=self._context.current_project.path,
            command=["uv", "add", "--upgrade-package", package_name, package_name],
        )

    def custom_commands(self) -> dict[str, CommandType]:
        return {}

    def _get_required_packages(self, group: Optional[str] = None) -> dict[str, str]:
        file_path = os.path.join(self._context.current_project.path, "pyproject.toml")
        with open(file_path, "rb") as file:
            data = tomllib.load(file)
        if group is None:
            dependencies = data["project"]["dependencies"]
        else:
            dependencies = data["tool"]["uv"][f"{group}-dependencies"]
        to_return = {}
        for dep in dependencies:
            if not isinstance(dep, str):
                continue
            match = re.match(r"^([a-zA-Z0-9_\-]+)(.*)$", dep)
            if match:
                package_name = match.group(1)
                version = match.group(2).strip() if match.group(2).strip() else "*"
                to_return[package_name] = version

        return to_return

    def _get_locked_versions(self) -> dict[str, str]:
        file_path = os.path.join(self._context.current_project.path, "uv.lock")
        with open(file_path, "rb") as file:
            data = tomllib.load(file)

        packages = data.get("package", [])
        return {
            pkg["name"]: pkg["version"]
            for pkg in packages
            if "name" in pkg and "version" in pkg
        }

    def _get_updatable_versions(self) -> dict[str, str]:
        project = self._context.current_project

        if self._context.uv_updatable_packages is not None:
            return self._context.uv_updatable_packages

        with subprocess.Popen(
            ["uv", "pip", "list", "--outdated", "--format=json"],
            cwd=project.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as process:
            stdout, stderr = process.communicate()
            return {
                package["name"]: package["latest_version"]
                for package in json.loads(stdout.strip())
            }
