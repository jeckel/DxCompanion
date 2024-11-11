from typing import Union, Optional
from dataclasses import dataclass

from .project import Project


@dataclass
class ShellCommand:
    path: str
    command: str
    shell: bool = True
    label: Optional[str] = None

    def __str__(self):
        return self.command


@dataclass
class NonShellCommand:
    path: str
    command: list[str]
    shell: bool = False
    label: Optional[str] = None

    def __str__(self):
        return " ".join(self.command)


CommandType = Union[ShellCommand, NonShellCommand]
