import subprocess

from models import Project
from models.composer import Composer
from .base_service import BaseService


class ComposerClient(BaseService):
    @staticmethod
    def updatable_packages(project: Project) -> dict[str, str]:
        with subprocess.Popen(
            ["composer", "update", "--dry-run"],
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
                    # Extract package name and target version
                    parts = line.split("(")
                    package_name = line.strip().split(" ")[2]  # Get the package name
                    version_info = (
                        parts[1].strip().rstrip(")")
                    )  # Get the version info (v2.2.9 => v2.3.0)
                    target_version = version_info.split("=>")[
                        -1
                    ].strip()  # Get the target version

                    # Append to the packages list as a dictionary
                    packages[package_name] = target_version
            return packages

    def composer_json(self, project: Project) -> None | Composer:
        if not project.composer:
            return None
        return Composer.from_json(project.path)
