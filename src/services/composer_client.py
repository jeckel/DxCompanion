import subprocess
from uuid import UUID

from models import Project
from models.composer import Composer
from .base_service import BaseService


class ComposerClient(BaseService):
    _updatable_packages: dict[UUID, dict[str, str]] = {}

    def updatable_packages(
        self, project: Project, no_cache: bool = False
    ) -> dict[str, str]:
        if project.id_ in self._updatable_packages is not None and not no_cache:
            return self._updatable_packages[project.id_]

        with subprocess.Popen(
            ["composer", "update", "--dry-run", "--no-ansi"],
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
            self._updatable_packages[project.id_] = packages
        return self._updatable_packages[project.id_]

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
