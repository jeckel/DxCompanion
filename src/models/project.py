import json
import os
from functools import cached_property
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class ProjectAction(BaseModel):
    label: str
    command: str
    help: Optional[str] = None
    use_shell: bool = False


class Project(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    path: str
    project_name: Optional[str] = None
    composer: Optional[bool] = Field(default=False)
    composer_cmd: list[str] = ["composer"]
    docker_composer_cmd: list[str] = ["docker", "compose"]
    actions: Optional[dict[str, list[ProjectAction]]] = None

    @classmethod
    def from_json(cls, json_path: str):
        with open(json_path, "r") as file:
            data = json.load(file)
            return cls(**data)

    @cached_property
    def name(self) -> str:
        return self.project_name or os.path.basename(self.path)

    @field_validator("path", mode="before")
    def check_directory_exists(cls, v) -> str:
        if not os.path.isdir(v):
            raise ValueError(f"Provided path '{v}' is not a valid directory.")
        return v

    @model_validator(mode="after")
    def check_composer_file(self):
        # Check if the directory contains a composer.json file
        composer_file = os.path.join(self.path, "composer.json")
        if os.path.exists(composer_file):
            self.composer = True
        return self

    # @cached_property
    # def composer_json(self) -> Optional[Composer]:
    #     if not self.composer:
    #         return None
    #     return Composer.from_json(self.path)
