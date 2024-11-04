from typing import Optional

from pydantic import BaseModel

from models import Project


class AppContext(BaseModel):
    project: Optional[Project] = None

    # Composer related context
    composer_updatable_packages: Optional[dict[str, str]] = None

    @property
    def current_project(self) -> Project:
        if self.project is None:
            raise RuntimeError("No project set in AppContext")
        return self.project
