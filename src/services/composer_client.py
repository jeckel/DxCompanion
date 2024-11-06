from __future__ import annotations
import subprocess

from models import Project
from models.app_context import AppContext
from models.composer import Composer
from .base_service import BaseService


class ComposerClient(BaseService):
    def __init__(self, context: AppContext):
        self._context = context

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

    @staticmethod
    def composer_json(project: Project) -> None | Composer:
        if not project.composer:
            return None
        return Composer.from_json(project.path)

    def scripts(self, project: Project) -> list[str]:
        composer = self.composer_json(project)
        if composer is None:
            return []
        return composer.manual_scripts
