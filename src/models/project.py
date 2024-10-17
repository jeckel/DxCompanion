import os
from functools import cached_property
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from models.composer import Composer


class Project(BaseModel):
    path: str
    composer: Optional[bool] = Field(default=False)

    @cached_property
    def name(self) -> str:
        return os.path.basename(self.path)

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

    @cached_property
    def composer_json(self) -> Optional[Composer]:
        if not self.composer:
            return None
        return Composer.from_json(self.path)
