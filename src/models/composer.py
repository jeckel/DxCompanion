import json
import os

from pydantic import BaseModel, Field
from rich import print

class Composer(BaseModel):
    project_path: str
    type: str
    license: str
    minimum_stability: str = Field(str, alias="minimum-stability")
    prefer_stable: bool = Field(False, alias="prefer-stable")
    required_packages: dict[str, str]
    required_packages_dev: dict[str, str]
    locked_packages: dict[str, str]
    locked_packages_dev: dict[str, str]
    scripts: dict[str, str|list[str]|dict[str, str]]

    @classmethod
    def from_json(cls, project_path: str):
        # json_path =
        with open(os.path.join(project_path, 'composer.json'), "r") as file:
            data = json.load(file)
            required_packages = data.pop("require", [])
            required_packages_dev = data.pop("require-dev", [])

        lock_file = os.path.join(project_path, 'composer.lock')
        if os.path.exists(lock_file):
            with open(lock_file, "r") as file:
                lock_data = json.load(file)
                locked_packages = {package['name']: package['version'] for package in lock_data.pop("packages", [])}
                locked_packages_dev = {package['name']: package['version'] for package in lock_data.pop("packages-dev", [])}

        return cls(
            project_path=project_path,
            required_packages_dev=required_packages_dev,
            required_packages=required_packages,
            locked_packages=locked_packages,
            locked_packages_dev=locked_packages_dev,
            **data)

    @property
    def manual_scripts(self) -> list[str]:
        exclude = ("auto-scripts", "post-install-cmd", "post-update-cmd")
        return list(filter(lambda x: x not in exclude, list(self.scripts.keys())))
        # return list(self.scripts.keys())
