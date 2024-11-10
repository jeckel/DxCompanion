from typing import Union
from dataclasses import dataclass

from .project import Project


@dataclass
class ShellCommand:
    path: str
    command: str
    shell: bool = True

    def __str__(self):
        return self.command


@dataclass
class NonShellCommand:
    path: str
    command: list[str]
    shell: bool = False

    def __str__(self):
        return " ".join(self.command)


CommandType = Union[ShellCommand, NonShellCommand]
